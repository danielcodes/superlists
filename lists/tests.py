from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, List

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        #content returns bytes, decode to python unicode string

class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        #the item has a list??
        #what the heck does .list do???
        #item has a list
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        #second item's list is also list_
        second_item.list = list_
        second_item.save()

        #first list
        #get first list
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        #create a url for a unique list, base on the db's id
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')


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


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        #posting to wrong url though
        self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        #need to create this new url
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        new_list = List.objects.first()
        #redirect to a new url
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

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

        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)
    


