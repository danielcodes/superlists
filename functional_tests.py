from selenium import webdriver
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

        #page titel says to-do list
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        #invite Tony to place an item on the list, he types "Kendama tricks to learn"
        #on enter, the page updates -> '1. Kendama tricks to learn'
        #there's still a textbox for more entries, he types, 'Around Japan'
        #now both items display on the list
        #will this list be remembered?, Tony sees a unique generated url
        #Tony visits the url, his todo list are there
        #Over

if __name__ == '__main__':
    unittest.main()


