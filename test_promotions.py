"""Unit tests for the promotions."""

import pytest

from products import NonStockedProduct, Product
from promotions import PercentDiscount, Promotion, SecondHalfPrice, ThirdOneFree


def test_promotion_is_abstract():
    """The abstract class Promotion cannot be instantiated."""
    with pytest.raises(TypeError):
        Promotion("General promotion")


def test_percent_discount():
    """A percent discount reduces the total price by the percentage."""
    product = Product("MacBook Air M2", price=1000, quantity=100)
    promotion = PercentDiscount("30% off!", percent=30)

    assert promotion.apply_promotion(product, 2) == 1400


def test_percent_discount_invalid_percent():
    """A percentage below 0 or above 100 raises an exception."""
    with pytest.raises(ValueError):
        PercentDiscount("Too much", percent=120)

    with pytest.raises(ValueError):
        PercentDiscount("Negative", percent=-5)


def test_second_half_price():
    """Every second item costs half the price."""
    product = Product("MacBook Air M2", price=1000, quantity=100)
    promotion = SecondHalfPrice("Second Half price!")

    assert promotion.apply_promotion(product, 1) == 1000
    assert promotion.apply_promotion(product, 2) == 1500
    assert promotion.apply_promotion(product, 3) == 2500


def test_third_one_free():
    """Every third item is free."""
    product = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    promotion = ThirdOneFree("Third One Free!")

    assert promotion.apply_promotion(product, 2) == 500
    assert promotion.apply_promotion(product, 3) == 500
    assert promotion.apply_promotion(product, 4) == 750


def test_buy_uses_promotion():
    """Buying a product with a promotion returns the reduced price."""
    product = Product("MacBook Air M2", price=1000, quantity=100)
    product.set_promotion(SecondHalfPrice("Second Half price!"))

    assert product.buy(2) == 1500
    assert product.get_quantity() == 98


def test_promotion_can_be_removed():
    """After removing the promotion the normal price applies again."""
    product = Product("MacBook Air M2", price=1000, quantity=100)
    product.set_promotion(SecondHalfPrice("Second Half price!"))

    product.set_promotion(None)

    assert product.get_promotion() is None
    assert product.buy(2) == 2000


def test_same_promotion_for_several_products():
    """One promotion can be used for more than one product."""
    promotion = PercentDiscount("50% off!", percent=50)
    mac = Product("MacBook Air M2", price=1000, quantity=100)
    license_key = NonStockedProduct("Windows License", price=100)
    mac.set_promotion(promotion)
    license_key.set_promotion(promotion)

    assert mac.buy(1) == 500
    assert license_key.buy(1) == 50
