"""Unit tests for the Product class."""

import pytest

from products import Product


def test_creating_prod():
    """A normal product is created with the given values and is active."""
    product = Product("MacBook Air M2", price=1450, quantity=100)

    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.get_quantity() == 100
    assert product.is_active()


def test_creating_prod_invalid_details():
    """An empty name or a negative price raises an exception."""
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)

    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_prod_becomes_inactive():
    """A product becomes inactive when its quantity reaches 0."""
    product = Product("MacBook Air M2", price=1450, quantity=5)

    product.buy(5)

    assert product.get_quantity() == 0
    assert not product.is_active()


def test_buy_modifies_quantity():
    """Buying reduces the quantity and returns the total price."""
    product = Product("MacBook Air M2", price=1450, quantity=100)

    total_price = product.buy(3)

    assert total_price == 4350
    assert product.get_quantity() == 97


def test_buy_too_much():
    """Buying more than the stock raises an exception and changes nothing."""
    product = Product("MacBook Air M2", price=1450, quantity=100)

    with pytest.raises(ValueError):
        product.buy(101)

    assert product.get_quantity() == 100
