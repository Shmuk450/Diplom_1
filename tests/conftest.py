# tests/conftest.py
import pytest
from unittest.mock import MagicMock
from praktikum.burger import Burger

@pytest.fixture
def bun_factory():
    """Фабрика моков булочек: bun = bun_factory(name, price)"""
    def _make(name: str = "white bun", price: float = 50.0):
        bun = MagicMock()
        bun.get_name.return_value = name
        bun.get_price.return_value = price
        return bun
    return _make

@pytest.fixture
def ingredient_factory():
    """Фабрика моков ингредиентов: ing = ingredient_factory(tp, name, price)"""
    def _make(tp: str = "FILLING", name: str = "cheese", price: float = 10.0):
        ing = MagicMock()
        ing.get_type.return_value = tp
        ing.get_name.return_value = name
        ing.get_price.return_value = price
        return ing
    return _make

@pytest.fixture
def burger():
    """Готовый экземпляр бургера для тестов"""
    return Burger()