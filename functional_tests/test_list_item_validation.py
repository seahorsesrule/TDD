from .base import FunctionalTest
from unittest import skip

class ItemValidationTest(FunctionalTest):

    @skip
    def test_cannot_add_empty_list_items(self):
        # Bill and Ted go to the homepage and accidentally try to submit
        # an empty list item. They hit enter on the empty input box.

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank

        # They try again with some text for the item, which now works

        # Perversely, they now decide to submit a second blank list item

        # They receive a similar warning on the list page

        # And she can correct it by filling some text in
        self.fail('write me')