from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase):

    #tests that root goes to home page?
    #in pipe, I can test that / goes to app.view index?
    #can test that all url paths resolve properly, there's quite a few
    def test_root_url_resolves_to_home_page_view(self):
        #resolves url path to corresponding function
        found = resolve('/')
        # print found
        # print found.func
        # print home_page
        self.assertEqual(found.func, home_page)

    #call the homepage view, and checking that it has the correct html
    #can be applied to each page in pipeline
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        #content returns bytes, decode to python unicode string
        self.assertEqual(response.content.decode(), expected_html)


#create a list and pass it to a url path
#check that it is using the respective template
#on pipe, can do the same with all viwes that require a parameter
#newspaper, images, cool
class ListViewTest(TestCase):

    def test_uses_list_template(self):
        #create a url for a unique list, base on the db's id
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    #create objects belonging to different views
    #check that they belong there and only there
    def test_displays_only_items_for_that_list(self):
        #creating two lists
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        #go to the page with the first list
        response = self.client.get('/lists/%d/' % (correct_list.id,))

        #check!
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

#test that when you input an item it create a new list
class NewListTest(TestCase):

    #check that you can post an item
    def test_saving_a_POST_request(self):
        #posting to wrong url though
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    #check for a redirect after some user interaction
    #on pipe, from filterfeeds to userfeeds
    def test_redirects_after_POST(self):
        #need to create this new url
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        new_list = List.objects.first()
        #redirect to a new url
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

    #create a new post and pass an empty item
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    #check for an empty database    
    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)


#this test can be applied to images
class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        #create two lists
        other_list = List.objects.create()
        correct_list = List.objects.create()

        #base on a list id, go to a new view and add item
        self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        #should have 1 item
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    #can test everything that requires a redirect
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/add_item' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

    
    def test_passes_correct_list_to_template(self):
        #two lists
        other_list = List.objects.create()
        correct_list = List.objects.create()

        #this returns the full on html
        #checks that the correct list has been passed in the view
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)
    
