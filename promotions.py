"""Promotions that change the price of a product purchase."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Only needed for the type hints; a normal import would be circular,
    # because products.py already imports this module
    from products import Product


class Promotion(ABC):
    """Abstract base class for all promotions.

    A promotion has a name and knows how to calculate the price
    for a given quantity of a product.
    """

    def __init__(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError("Promotion name must be a string.")
        if not name.strip():
            raise ValueError("Promotion name must not be empty.")
        self.name = name

    @abstractmethod
    def apply_promotion(self, product: Product, quantity: int) -> float:
        """Return the total price for the quantity after the promotion."""


class PercentDiscount(Promotion):
    """A discount of a fixed percentage, e.g. 30 % off."""

    def __init__(self, name: str, percent: float) -> None:
        super().__init__(name)
        if not isinstance(percent, (int, float)):
            raise TypeError("Percent must be a number.")
        if percent < 0 or percent > 100:
            raise ValueError("Percent must be between 0 and 100.")
        self.percent = percent

    def apply_promotion(self, product: Product, quantity: int) -> float:
        """Return the total price reduced by the percentage."""
        full_price = product.price * quantity
        return float(full_price * (1 - self.percent / 100))


class SecondHalfPrice(Promotion):
    """Every second item costs only half the price."""

    def apply_promotion(self, product: Product, quantity: int) -> float:
        """Return the total price with every second item at half price."""
        half_price_items = quantity // 2
        full_price_items = quantity - half_price_items
        return float(
            product.price * full_price_items + product.price * 0.5 * half_price_items
        )


class ThirdOneFree(Promotion):
    """Buy two, get the third one for free."""

    def apply_promotion(self, product: Product, quantity: int) -> float:
        """Return the total price with every third item for free."""
        free_items = quantity // 3
        return float(product.price * (quantity - free_items))
