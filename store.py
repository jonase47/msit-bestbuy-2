"""Store class that holds and manages products."""


class Store:
    """A store containing a list of products."""

    def __init__(self, product_list):
        self.products = list(product_list)

    def add_product(self, product):
        """Add a product to the store."""
        self.products.append(product)

    def remove_product(self, product):
        """Remove a product from the store."""
        if product not in self.products:
            raise ValueError(f"{product.name} is not in the store.")
        self.products.remove(product)

    def get_total_quantity(self):
        """Return the total number of items of all active products."""
        total = 0
        for product in self.products:
            if product.is_active():
                total += product.get_quantity()
        return total

    def get_all_products(self):
        """Return all active products."""
        active_products = []
        for product in self.products:
            if product.is_active():
                active_products.append(product)
        return active_products

    def order(self, shopping_list):
        """Buy a list of (product, quantity) tuples and return the total price.

        The order is all or nothing: every position is checked first,
        and only if all of them are fine the products are bought.
        """
        # Step 1: sum up the quantities per product, in case the same
        # product appears more than once in the shopping list
        requested = {}
        for product, quantity in shopping_list:
            if product not in self.products:
                raise ValueError(f"{product.name} is not in the store.")
            if quantity <= 0:
                raise ValueError("Quantity to buy must be greater than 0.")
            requested[product] = requested.get(product, 0) + quantity

        # Step 2: check everything, nothing is changed yet
        for product, quantity in requested.items():
            product.check_purchase(quantity)

        # Step 3: buy
        total_price = 0.0
        for product, quantity in requested.items():
            total_price += product.buy(quantity)
        return total_price
