import unittest

from shopping_cart import ShoppingCartConcreteCreator
from test_utils import Capturing


class ShoppingCartTest(unittest.TestCase):
    def test_print_receipt(self):
        sc = ShoppingCartConcreteCreator().operation()
        sc.add_item("apple", 2)
        with Capturing() as output:
            sc.print_receipt()
        self.assertEqual("apple - 2 - 100", output[0])

    def test_doesnt_explode_on_mystery_item(self):
        sc = ShoppingCartConcreteCreator().operation()
        sc.add_item("apple", 2)
        sc.add_item("banana", 5)
        sc.add_item("pear", 5)
        with Capturing() as output:
            sc.print_receipt()
        self.assertEqual("apple - 2 - 100", output[0])
        self.assertEqual("banana - 5 - 200", output[1])
        self.assertEqual("pear - 5 - 0", output[2])


    def test_print_total(self):
        sc = ShoppingCartConcreteCreator().operation()
        sc.add_item("apple", 2)
        sc.add_item("banana", 5)

        with Capturing() as output:
            sc.print_receipt()

        # Taking into consideration the total line
        self.assertEqual("The total amount is: €12.00", output[-1])


    def test_preserve_items_order(self):
        # Regular order
        sc1 = ShoppingCartConcreteCreator().operation()
        sc1.add_item("banana", 5)
        sc1.add_item("apple", 2)

        with Capturing() as output:
            sc1.print_receipt()

        self.assertEqual("banana - 5 - 200", output[0])
        self.assertEqual("apple - 2 - 100", output[1])

        # Reversing the order
        sc2 = ShoppingCartConcreteCreator().operation()
        sc2.add_item("apple", 2)
        sc2.add_item("banana", 5)

        with Capturing() as output:
            sc2.print_receipt()

        self.assertEqual("apple - 2 - 100", output[0])
        self.assertEqual("banana - 5 - 200", output[1])


    def test_print_recipe_with_custom_formatting(self):
        my_pattern = "x%value% '%key%' (%price%)"
        sc = ShoppingCartConcreteCreator().operation()

        # Adding custom formatting
        sc.print_recipe_item_pattern = my_pattern

        sc.add_item("banana", 5)
        sc.add_item("apple", 2)

        with Capturing() as output:
            sc.print_receipt()

        # Checking the new formatting pattern
        self.assertEqual("x5 'banana' (200)", output[0])
        self.assertEqual("x2 'apple' (100)", output[1])


unittest.main(exit=False)
