from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Tony decides to check out a new todo list app
        self.browser.get(self.server_url)

        #page title and header says to-do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #invite Tony to place an item on the list        
        inputbox = self.get_item_input_box()
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        #he types "Kendama tricks to learn"
        inputbox.send_keys('Kendama tricks to learn')

        #on enter, the page updates -> '1. Kendama tricks to learn'
        #take to a new url
        inputbox.send_keys(Keys.ENTER)
        #checks that there has been a redirect
        edith_list_url = self.browser.current_url
        self.assertRegexpMatches(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Kendama tricks to learn')

        #there's still a textbox for more entries, he types, 'Around Japan'
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Around Japan')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('1: Kendama tricks to learn')
        self.check_for_row_in_list_table('2: Around Japan')

        #************************************************************************
        #new user coming along, Francis
        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc #1
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Kendama tricks', page_text)
        self.assertNotIn('to learn', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegexpMatches(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)


        #reminder message
        # self.fail('Finish the test!') 

