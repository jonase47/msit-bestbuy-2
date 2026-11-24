"""Unit tests for the Store class."""

import pytest

from products import LimitedProduct, Product
from store import Store


def test_total_quantity_counts_only_active_products():
    """Inactive products are not part of the total quantity."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    store = Store([mac, bose])

    bose.deactivate()

    assert store.get_total_quantity() == 100


def test_order_returns_total_price():
    """An order returns the sum of all positions and reduces the stock."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    store = Store([mac, bose])

    total_price = store.order([(mac, 1), (bose, 2)])

    assert total_price == 1950
    assert mac.quantity == 99
    assert bose.quantity == 498


def test_order_is_all_or_nothing():
    """If one position fails, no product of the order is bought."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    store = Store([mac, bose])

    with pytest.raises(ValueError):
        store.order([(mac, 1), (bose, 501)])

    assert mac.quantity == 100
    assert bose.quantity == 500


def test_order_sums_up_same_product():
    """The same product in two positions is checked with its total quantity."""
    mac = Product("MacBook Air M2", price=1450, quantity=5)
    store = Store([mac])

    with pytest.raises(ValueError):
        store.order([(mac, 3), (mac, 3)])

    assert mac.quantity == 5


def test_order_respects_limit_across_positions():
    """A limited product cannot exceed its maximum by splitting the order."""
    shipping = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    store = Store([shipping])

    with pytest.raises(ValueError):
        store.order([(shipping, 1), (shipping, 1)])

    assert shipping.quantity == 250


def test_order_rejects_negative_quantity():
    """A negative quantity is rejected, even if the sum would be positive."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    store = Store([mac])

    with pytest.raises(ValueError):
        store.order([(mac, 5), (mac, -2)])

    assert mac.quantity == 100


def test_order_rejects_product_not_in_store():
    """A product that is not part of the store cannot be ordered."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    pixel = Product("Google Pixel 7", price=500, quantity=250)
    store = Store([mac])

    with pytest.raises(ValueError):
        store.order([(pixel, 1)])


def test_product_in_store():
    """The in operator checks if a product is part of the store."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    pixel = Product("Google Pixel 7", price=500, quantity=250)
    store = Store([mac])

    assert mac in store
    assert pixel not in store


def test_add_two_stores():
    """Adding two stores returns a new store with the products of both."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel = Product("Google Pixel 7", price=500, quantity=250)
    first_store = Store([mac, bose])
    second_store = Store([bose, pixel])

    combined_store = first_store + second_store

    assert mac in combined_store
    assert bose in combined_store
    assert pixel in combined_store
    assert len(combined_store.get_all_products()) == 3
    # The original stores stay unchanged
    assert pixel not in first_store
    assert mac not in second_store
