from abc import ABC, abstractmethod
from collections import OrderedDict

from shopping_cart_interface import IShoppingCart
from pricer import Pricer


class ShoppingCart(IShoppingCart):
    """
    Implementation of the shopping tills in our supermarket.
    """

    # Static field print_recipe_item_pattern
    # The better need to contains variable like so.
    # The %key%, %value% and %price% will be replaced by the real scenario's values
    #   key : correspond to the name of the product
    #   value : correspond to the quantity of the product present in the shopping cart
    #   price : correspond to the price per unit of the product

    # E.g. "Product %key% \t(%price%) x%value%"
    # Will give an output like this:
    # "Product banana   (200) x5"
    # "Product apple    (100) x2"

    print_recipe_item_pattern = '%key% - %value% - %price%'

    def __init__(self, pricer: Pricer):
        self.pricer = pricer
        # Changing dict to OrderedDict
        self._contents: OrderedDict[str,int] = OrderedDict()

    def add_item(self, item_type: str, number: int):
        # adds new item to or update existing item in the shopping cart
        if item_type not in self._contents:
            self._contents[item_type] = number
        else:
            self._contents[item_type] = self._contents[item_type] + number

    def print_receipt(self):
        # Initializing the total
        total = 0

        for key, value in self._contents.items():
            price = self.pricer.get_price(key)
            item_repr = self.print_recipe_item_pattern \
                .replace('%key%', str(key)) \
                .replace('%value%', str(value)) \
                .replace('%price%', str(price))

            print(item_repr)

            # Adding to the total each time
            total += price * value

        # Calculating the total in €
        total = round(total / 100, 2)

        # Total Line
        print(f"The total amount is: €{total:.2f}")


class ShoppingCartCreator(ABC):
    """
    Interface for the ShoppingCart creator.
    The creation process will be delegated to the subclasses of this class.
    """
    @abstractmethod
    def factory_method(self) -> ShoppingCart:
        # return the ShoppingCart object
        pass

    def operation(self) -> ShoppingCart:
        # Here more operations can be performed on the ShoppingCart object
        # returns ShoppingCart object
        return self.factory_method()


class ShoppingCartConcreteCreator(ShoppingCartCreator):
    """
    Concrete class for the ShoppingCart creator.
    Implements the factory_method
    """
    def factory_method(self) -> ShoppingCart:
        # returns ShoppingCart object
        return ShoppingCart(Pricer())
