from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

#User Story
class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        #waits for site to load before checking things
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Tony decides to check out a new todo list app
        self.browser.get('http://localhost:8000')

        #page title and header says to-do list
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #invite Tony to place an item on the list        
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        #he types "Kendama tricks to learn"
        inputbox.send_keys('Kendama tricks to learn')

        #on enter, the page updates -> '1. Kendama tricks to learn'
        inputbox.send_keys(Keys.ENTER)

        #there's still a textbox for more entries, he types, 'Around Japan'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Around Japan')
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Kendama tricks to learn', [row.text for row in rows]) 
        self.assertIn('2: Around Japan', [row.text for row in rows])

        #reminder message
        self.fail('Finish the test!') 

        #now both items display on the list
        #will this list be remembered?, Tony sees a unique generated url
        #Tony visits the url, his todo list are there
        #Over

if __name__ == '__main__':
    unittest.main()


