"""Product classes for the store."""

from promotions import Promotion


class Product:
    """A product type with name, price, stock quantity and active status."""

    def __init__(self, name, price, quantity):
        # Check the type first (TypeError), then the value (ValueError)
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number.")
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be a whole number.")

        if not name.strip():
            raise ValueError("Name must not be empty.")
        if price < 0:
            raise ValueError("Price must not be negative.")
        if quantity < 0:
            raise ValueError("Quantity must not be negative.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True
        self.promotion = None

    def get_quantity(self):
        """Return the stock quantity."""
        return self.quantity

    def set_quantity(self, quantity):
        """Set the stock quantity; deactivate the product at 0."""
        if not isinstance(quantity, int):
            raise TypeError("Quantity must be a whole number.")
        if quantity < 0:
            raise ValueError("Quantity must not be negative.")
        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()

    def is_active(self):
        """Return True if the product is active."""
        return self.active

    def activate(self):
        """Activate the product."""
        self.active = True

    def deactivate(self):
        """Deactivate the product."""
        self.active = False

    def get_promotion(self):
        """Return the current promotion, or None if there is none."""
        return self.promotion

    def set_promotion(self, promotion):
        """Set the promotion of the product; None removes it."""
        if promotion is not None and not isinstance(promotion, Promotion):
            raise TypeError("Promotion must be a Promotion or None.")
        self.promotion = promotion

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
        # Use the setter so the product gets deactivated when sold out
        self.set_quantity(self.quantity - quantity)
        return total_price


class NonStockedProduct(Product):
    """A product without stock, e.g. a software license.

    Its quantity is always 0 and it can be bought in any amount.
    """

    def __init__(self, name, price):
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity):
        """The quantity of a non-stocked product always stays 0."""
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
