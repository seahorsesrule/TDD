from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):

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
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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