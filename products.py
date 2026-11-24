"""Product classes for the store."""

from promotions import Promotion


class Product:
    """A product type with name, price, stock quantity and active status."""

    def __init__(self, name, price, quantity):
        self._active = True
        self._promotion = None
        # These assignments run through the property setters below,
        # so every value is checked there
        self.name = name
        self.price = price
        self.quantity = quantity

    @property
    def name(self):
        """The name of the product."""
        return self._name

    @name.setter
    def name(self, name):
        # Check the type first (TypeError), then the value (ValueError)
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not name.strip():
            raise ValueError("Name must not be empty.")
        self._name = name

    @property
    def price(self):
        """The price of a single item."""
        return self._price

    @price.setter
    def price(self, price):
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number.")
        if price < 0:
            raise ValueError("Price must not be negative.")
        self._price = price

    @property
    def quantity(self):
        """The stock quantity; setting it to 0 deactivates the product."""
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be a whole number.")
        if quantity < 0:
            raise ValueError("Quantity must not be negative.")
        self._quantity = quantity
        if self._quantity == 0:
            self.deactivate()

    @property
    def active(self):
        """True if the product is active (read-only, see activate/deactivate)."""
        return self._active

    def activate(self):
        """Activate the product."""
        self._active = True

    def deactivate(self):
        """Deactivate the product."""
        self._active = False

    @property
    def promotion(self):
        """The current promotion, or None if there is none."""
        return self._promotion

    @promotion.setter
    def promotion(self, promotion):
        if promotion is not None and not isinstance(promotion, Promotion):
            raise TypeError("Promotion must be a Promotion or None.")
        self._promotion = promotion

    def get_promotion_name(self):
        """Return the name of the current promotion, or "None"."""
        if self.promotion is None:
            return "None"
        return self.promotion.name

    def calculate_price(self, quantity):
        """Return the total price for the quantity, including a promotion."""
        if self.promotion is None:
            return float(self.price * quantity)
        return self.promotion.apply_promotion(self, quantity)

    def __str__(self):
        """Return the product as text, so that print(product) works."""
        return (
            f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}, "
            f"Promotion: {self.get_promotion_name()}"
        )

    def __gt__(self, other):
        """Return True if this product is more expensive than the other."""
        if not isinstance(other, Product):
            return NotImplemented
        return self.price > other.price

    def __lt__(self, other):
        """Return True if this product is cheaper than the other."""
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price

    def check_purchase(self, quantity):
        """Raise an error if the given quantity cannot be bought.

        Only checks, changes nothing. This lets the store validate a
        whole order before the first product is actually bought.
        """
        if not isinstance(quantity, int):
            raise TypeError("Quantity to buy must be a whole number.")
        if not self.active:
            raise ValueError(f"{self.name} is not active and cannot be bought.")
        if quantity <= 0:
            raise ValueError("Quantity to buy must be greater than 0.")
        self.check_stock(quantity)

    def check_stock(self, quantity):
        """Raise a ValueError if there is not enough stock for the quantity."""
        if quantity > self.quantity:
            raise ValueError(
                f"Not enough in stock: {self.quantity} available, {quantity} requested."
            )

    def buy(self, quantity):
        """Buy the given quantity and return the total price."""
        self.check_purchase(quantity)

        total_price = self.calculate_price(quantity)
        # The quantity setter deactivates the product when it is sold out
        self.quantity -= quantity
        return total_price


class NonStockedProduct(Product):
    """A product without stock, e.g. a software license.

    Its quantity is always 0 and it can be bought in any amount.
    """

    def __init__(self, name, price):
        super().__init__(name, price, quantity=0)

    @property
    def quantity(self):
        """The quantity of a non-stocked product is always 0."""
        return 0

    @quantity.setter
    def quantity(self, quantity):
        if quantity != 0:
            raise ValueError(f"{self.name} is not stocked, its quantity stays 0.")

    def check_stock(self, quantity):
        """Non-stocked products never run out, so there is nothing to check."""

    def __str__(self):
        """Return the product as text, so that print(product) works."""
        return (
            f"{self.name}, Price: ${self.price}, Quantity: Unlimited, "
            f"Promotion: {self.get_promotion_name()}"
        )

    def buy(self, quantity):
        """Buy the given quantity and return the total price."""
        self.check_purchase(quantity)
        return self.calculate_price(quantity)


class LimitedProduct(Product):
    """A product that can only be bought a limited number of times per order."""

    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        if not isinstance(maximum, int):
            raise TypeError("Maximum must be a whole number.")
        if maximum < 1:
            raise ValueError("Maximum must be at least 1.")
        self.maximum = maximum

    def check_purchase(self, quantity):
        """Raise an error if the quantity cannot be bought or is over the limit."""
        super().check_purchase(quantity)
        if quantity > self.maximum:
            raise ValueError(
                f"{self.name} is limited to {self.maximum} per order, {quantity} requested."
            )

    def __str__(self):
        """Return the product as text, so that print(product) works."""
        return (
            f"{self.name}, Price: ${self.price}, Limited to {self.maximum} per order!, "
            f"Promotion: {self.get_promotion_name()}"
        )
