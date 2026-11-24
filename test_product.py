"""Unit tests for the Product class."""

import pytest

from products import LimitedProduct, NonStockedProduct, Product


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


def test_creating_prod_wrong_types():
    """A wrong type for name, price or quantity raises a TypeError."""
    with pytest.raises(TypeError):
        Product(123, price=1450, quantity=100)

    with pytest.raises(TypeError):
        Product("MacBook Air M2", price="1450", quantity=100)

    with pytest.raises(TypeError):
        Product("MacBook Air M2", price=1450, quantity=1.5)


def test_non_stocked_prod_has_no_quantity():
    """A non-stocked product has quantity 0 and is still active."""
    product = NonStockedProduct("Windows License", price=125)

    assert product.get_quantity() == 0
    assert product.is_active()


def test_non_stocked_prod_can_always_be_bought():
    """Buying a non-stocked product works for any amount and keeps quantity 0."""
    product = NonStockedProduct("Windows License", price=125)

    total_price = product.buy(1000)

    assert total_price == 125000
    assert product.get_quantity() == 0
    assert product.is_active()


def test_limited_prod_within_limit():
    """A limited product can be bought up to its maximum."""
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)

    total_price = product.buy(1)

    assert total_price == 10
    assert product.get_quantity() == 249


def test_limited_prod_over_limit():
    """Buying more than the maximum raises an exception and changes nothing."""
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)

    with pytest.raises(ValueError):
        product.buy(2)

    assert product.get_quantity() == 250


def test_str_shows_product_details():
    """str() returns the text that print() shows for each product type."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    license_key = NonStockedProduct("Windows License", price=125)
    shipping = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)

    assert str(mac) == "MacBook Air M2, Price: $1450, Quantity: 100, Promotion: None"
    assert str(license_key) == (
        "Windows License, Price: $125, Quantity: Unlimited, Promotion: None"
    )
    assert str(shipping) == "Shipping, Price: $10, Limited to 1 per order!, Promotion: None"


def test_compare_products_by_price():
    """Products are compared by their price with > and <."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)

    assert mac > bose
    assert bose < mac
    assert not mac < bose


def test_compare_product_with_number_fails():
    """Comparing a product with something else raises a TypeError."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    with pytest.raises(TypeError):
        assert mac > 1000
