"""Command-line interface for the Best Buy store."""

from collections.abc import Callable

import products
import promotions
import store


def list_products(store_obj: store.Store) -> list[products.Product]:
    """Print all active products numbered and return them."""
    print("------")
    active_products = store_obj.get_all_products()
    number = 1
    for product in active_products:
        print(f"{number}. {product}")
        number += 1
    print("------")
    return active_products


def show_total(store_obj: store.Store) -> None:
    """Print the total amount of items in the store."""
    print(f"Total of {store_obj.get_total_quantity()} items in store")


def make_order(store_obj: store.Store) -> None:
    """Ask the user for products and quantities, then place the order."""
    active_products = list_products(store_obj)
    print("When you want to finish order, enter empty text.")

    shopping_list = []
    while True:
        # Check every input right away: an empty input ends the order
        product_input = input("Which product # do you want? ").strip()
        if not product_input:
            break
        amount_input = input("What amount do you want? ").strip()
        if not amount_input:
            break

        try:
            product_index = int(product_input) - 1
            amount = int(amount_input)
        except ValueError:
            print("Please enter numbers only.")
            continue

        if product_index < 0 or product_index >= len(active_products):
            print("This product number does not exist.")
            continue

        product = active_products[product_index]
        # Check the position right away, so the user gets direct feedback
        try:
            product.check_purchase(amount)
        except ValueError as error:
            print(f"Error adding product! {error}\n")
            continue

        shopping_list.append((product, amount))
        print("Product added to list!\n")

    if len(shopping_list) == 0:
        print("No products ordered.")
        return

    try:
        total_price = store_obj.order(shopping_list)
        print(f"********\nOrder made! Total payment: ${total_price}")
    except ValueError as error:
        print(f"Error while making order! {error}")


# Dispatch table: menu choice -> function that handles it
MENU_ACTIONS: dict[str, Callable[[store.Store], object]] = {
    "1": list_products,
    "2": show_total,
    "3": make_order,
}


def start(store_obj: store.Store) -> None:
    """Show the main menu until the user quits."""
    while True:
        print("\n   Store Menu")
        print("   ----------")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Please choose a number: ").strip()

        if choice == "4":
            print("Bye!")
            break

        action = MENU_ACTIONS.get(choice)
        if action is None:
            print("Invalid choice, please choose a number from 1 to 4.")
        else:
            action(store_obj)


def main() -> None:
    """Create the initial inventory and start the store menu."""
    # setup initial stock of inventory
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250),
        products.NonStockedProduct("Windows License", price=125),
        products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1),
    ]

    # Create promotion catalog
    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].promotion = second_half_price
    product_list[1].promotion = third_one_free
    product_list[3].promotion = thirty_percent

    best_buy = store.Store(product_list)
    start(best_buy)


if __name__ == "__main__":
    main()
