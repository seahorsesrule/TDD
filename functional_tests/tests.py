from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Rufus has returned from the future with a message for Bill and Ted that there is a cool new
        # online to-do app they should use to organize their excellent time traveling adventures.
        # They go check out its homepage
        self.browser.get(self.live_server_url)

        # They notice the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # They are able to enter a to-do item right away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # They type "Visit North Korea 1948" into a text box
        inputbox.send_keys('Visit North Korea 1948')

        # When they hit enter, the page updates, and now the page lists
        # "1. Visit North Korea 1948" as a to-do list item
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1. Visit North Korea 1948')

        # There is still a text-box for them to enter another item. They enter,
        # "Assassinate Kim Il-sung"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Assassinate Kim Il-sung')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on their list
        self.check_for_row_in_list_table('1. Visit North Korea 1948')
        self.check_for_row_in_list_table('2. Assassinate Kim Il-sung')

        # Bill and Ted wonder whether the site will remember their list. Then they see that
        # the site has generated a unique URL for them -- there is some explanatory text to that effect
        self.fail('Finish the test!')

        # They visit the URL - their to-do list is still there.

        # Satisfied, they party on.