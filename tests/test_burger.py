import pytest
from unittest.mock import MagicMock
from praktikum.burger import Burger

# --- фабрики моков ---
def make_bun(name: str, price: float):
    bun = MagicMock()
    bun.get_name.return_value = name
    bun.get_price.return_value = price
    return bun

def make_ingredient(tp: str, name: str, price: float):
    ing = MagicMock()
    ing.get_type.return_value = tp
    ing.get_name.return_value = name
    ing.get_price.return_value = price
    return ing


class TestBurger:
    def test_set_buns_and_price_without_ingredients(self):
        b = Burger()
        b.set_buns(make_bun("black bun", 100))
        assert b.bun is not None
        assert b.get_price() == 200  # две половинки булки

    def test_add_ingredient_appends(self):
        b = Burger()
        b.set_buns(make_bun("white bun", 50))
        ing = make_ingredient("SAUCE", "hot", 10)
        b.add_ingredient(ing)
        assert b.ingredients == [ing]

    def test_remove_ingredient_by_index(self):
        b = Burger()
        b.set_buns(make_bun("white bun", 50))
        a = make_ingredient("SAUCE", "A", 1)
        c = make_ingredient("FILLING", "C", 3)
        b.add_ingredient(a)
        b.add_ingredient(c)

        b.remove_ingredient(0)
        assert [i.get_name() for i in b.ingredients] == ["C"]

    @pytest.mark.parametrize(
        "initial_names, src, dst, expected",
        [
            (["a", "b", "c"], 0, 2, ["b", "c", "a"]),      # первый в конец
            (["a", "b", "c"], 2, 0, ["c", "a", "b"]),      # последний в начало
            (["a", "b", "c", "d"], 1, 2, ["a", "c", "b", "d"]),  # соседние
        ],
    )
    def test_move_ingredient_reorders(self, initial_names, src, dst, expected):
        b = Burger()
        b.set_buns(make_bun("white bun", 50))
        for name in initial_names:
            b.add_ingredient(make_ingredient("FILLING", name, 1))

        b.move_ingredient(src, dst)
        assert [i.get_name() for i in b.ingredients] == expected

    @pytest.mark.parametrize(
        "bun_price, items",
        [
            (100, []),
            (50,  [("SAUCE", "hot", 10), ("FILLING", "cheese", 30)]),
            (80,  [("FILLING", "cutlet", 120), ("SAUCE", "spicy", 15), ("FILLING", "salad", 5)]),
        ],
    )
    def test_get_price_totals(self, bun_price, items):
        b = Burger()
        b.set_buns(make_bun("any", bun_price))
        total = 0
        for tp, name, price in items:
            b.add_ingredient(make_ingredient(tp, name, price))
            total += price

        assert b.get_price() == bun_price * 2 + total

    def test_get_receipt_signatures(self):
        """
        Проверяем сигнатуры чека (без пиксель-перфекта):
        - верх/низ булки
        - строки ингредиентов: '= sauce <name> =' и '= filling <name> ='
        - строку цены 'Price: <число>'
        """
        b = Burger()
        bun = make_bun("black bun", 100)
        b.set_buns(bun)

        sauce = make_ingredient("SAUCE", "hot sauce", 20)
        filling = make_ingredient("FILLING", "cutlet", 80)
        b.add_ingredient(sauce)
        b.add_ingredient(filling)

        expected_price = 2 * 100 + 20 + 80  # 300
        receipt = b.get_receipt()

        top_bottom = f"(==== {bun.get_name()} ====)"
        assert top_bottom in receipt
        assert receipt.count(top_bottom) >= 2

        # типы приводятся к lower() в Burger.get_receipt()
        assert "= sauce hot sauce =" in receipt.lower()
        assert "= filling cutlet =" in receipt.lower()

        assert f"Price: {expected_price}" in receipt