from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Rufus has returned from the future with a message for Bill and Ted that there is a cool new
        # online to-do app they should use to organize their excellent time traveling adventures.
        # They go check out its homepage
        self.browser.get('http://localhost:8000')

        # They notice the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # They are able to enter a to-do item right away

        # They type "Visit North Korea 1948" into a text box

        # When they hit enter, the page updates, and now the page lists
        # "1. Visit North Korea 1948" as a to-do list item

        # There is still a text-box for them to enter another item. They enter,
        # "Assassinate Kim Il-sung"

        # The page updates again, and now shows both items on their list

        # Bill and Ted wonder whether the site will remember their list. Then they see that
        # the site has generated a unique URL for them -- there is some explanatory text to that effect

        # They visit the URL - their to-do list is still there.

        # Satisfied, they party on.

if __name__ == '__main__':
    unittest.main(warnings='ignore')