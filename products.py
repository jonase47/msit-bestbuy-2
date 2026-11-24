"""Product class for the store."""


class Product:
    """A product type with name, price, stock quantity and active status."""

    def __init__(self, name, price, quantity):
        if not name or not name.strip():
            raise ValueError("Name must not be empty.")
        if price < 0:
            raise ValueError("Price must not be negative.")
        if quantity < 0:
            raise ValueError("Quantity must not be negative.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self):
        """Return the stock quantity."""
        return self.quantity

    def set_quantity(self, quantity):
        """Set the stock quantity; deactivate the product at 0."""
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

    def show(self):
        """Print the product to the console."""
        print(f"{self.name}, Price: {self.price}, Quantity: {self.quantity}")

    def buy(self, quantity):
        """Buy the given quantity and return the total price."""
        if not self.active:
            raise ValueError(f"{self.name} is not active and cannot be bought.")
        if quantity <= 0:
            raise ValueError("Quantity to buy must be greater than 0.")
        if quantity > self.quantity:
            raise ValueError(
                f"Not enough in stock: {self.quantity} available, {quantity} requested."
            )

        total_price = self.price * quantity
        # Use the setter so the product gets deactivated when sold out
        self.set_quantity(self.quantity - quantity)
        return float(total_price)
