from django.contrib.staticfiles.testing import StaticLiveServerCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys

class NewVisitorTest(StaticLiveServerCase):

    # allows use of servers besides django test server
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super().setUpClass()
        cls.server_url = cls.live_server_url

    # allows use of servers besides django test server
    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

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
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024,768)

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
        billted_list_url = self.browser.current_url
        self.assertRegex(billted_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1. Visit North Korea 1948')

        # There is still a text-box for them to enter another item. They enter,
        # "Assassinate Kim Il-sung"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Assassinate Kim Il-sung')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on their list
        self.check_for_row_in_list_table('1. Visit North Korea 1948')
        self.check_for_row_in_list_table('2. Assassinate Kim Il-sung')

        # Now a new user, Rufus, comes along to the site.

        ## We use a new browser session to make sure that no information of
        ## Bill and Ted is coming through from cookies et. #
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Rufus visits the home page. There is no sign of Bill and Ted's list.
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Visit North Korea 1948', page_text)
        self.assertNotIn('Assassinate Kim Il-sung', page_text)

        # Rufus starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Be excellent to each other')
        inputbox.send_keys(Keys.ENTER)

        # Rufus gets his own unique URL
        rufus_list_url = self.browser.current_url
        self.assertRegex(rufus_list_url, '/lists/.+')
        self.assertNotEqual(rufus_list_url, billted_list_url)

        # Again, there is no trace of Bill and Ted's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Visit North Korea 1948', page_text)
        self.assertIn('Be excellent to each other', page_text)

        # Satisfied, they all party on.

    def test_layout_and_styling(self):
        # Bill and Ted go to the home page
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # They notice the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )

        # They start a new list and notice the input is centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5
        )