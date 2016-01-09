from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List

class ListAndItemModelsTest(TestCase):

    #throw data in, and check data out
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
        #testing constangs here aren't we
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()



