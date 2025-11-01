# tests/test_burger.py
import pytest


class TestBurger:
    def test_set_buns_and_price_without_ingredients(self, burger, bun_factory):
        b = burger
        b.set_buns(bun_factory("black bun", 100))
        assert b.bun is not None
        assert b.get_price() == 200

    def test_add_ingredient_appends(self, burger, bun_factory, ingredient_factory):
        b = burger
        b.set_buns(bun_factory("white bun", 50))
        ing = ingredient_factory("SAUCE", "hot", 10)
        b.add_ingredient(ing)
        assert b.ingredients == [ing]

    def test_remove_ingredient_by_index(self, burger, bun_factory, ingredient_factory):
        b = burger
        b.set_buns(bun_factory("white bun", 50))
        a = ingredient_factory("SAUCE", "A", 1)
        c = ingredient_factory("FILLING", "C", 3)
        b.add_ingredient(a)
        b.add_ingredient(c)

        b.remove_ingredient(0)
        assert [i.get_name() for i in b.ingredients] == ["C"]

    @pytest.mark.parametrize(
        "initial_names, src, dst, expected",
        [
            (["a", "b", "c"], 0, 2, ["b", "c", "a"]),
            (["a", "b", "c"], 2, 0, ["c", "a", "b"]),
            (["a", "b", "c", "d"], 1, 2, ["a", "c", "b", "d"]),
        ],
    )
    def test_move_ingredient_reorders(
        self, burger, bun_factory, ingredient_factory, initial_names, src, dst, expected
    ):
        b = burger
        b.set_buns(bun_factory("white bun", 50))
        for name in initial_names:
            b.add_ingredient(ingredient_factory("FILLING", name, 1))

        b.move_ingredient(src, dst)
        assert [i.get_name() for i in b.ingredients] == expected

    @pytest.mark.parametrize(
        "bun_price, items",
        [
            (100, []),
            (50, [("SAUCE", "hot", 10), ("FILLING", "cheese", 30)]),
            (
                80,
                [
                    ("FILLING", "cutlet", 120),
                    ("SAUCE", "spicy", 15),
                    ("FILLING", "salad", 5),
                ],
            ),
        ],
    )
    def test_get_price_totals(self, burger, bun_factory, ingredient_factory, bun_price, items):
        b = burger
        b.set_buns(bun_factory("any", bun_price))
        total = 0
        for tp, name, price in items:
            b.add_ingredient(ingredient_factory(tp, name, price))
            total += price
        assert b.get_price() == bun_price * 2 + total

    def test_get_receipt_signatures(self, burger, bun_factory, ingredient_factory):
        """
        Проверяем полное содержимое чека и порядок строк:
        - верхняя булка
        - ингредиенты
        - нижняя булка
        - итоговая цена
        """
        b = burger
        bun = bun_factory("black bun", 100)
        b.set_buns(bun)

        sauce = ingredient_factory("SAUCE", "hot sauce", 20)
        filling = ingredient_factory("FILLING", "cutlet", 80)
        b.add_ingredient(sauce)
        b.add_ingredient(filling)

        expected_price = 2 * 100 + 20 + 80  # 300
        receipt = b.get_receipt()

        # нормализуем чек в список строк
        lines = [ln.strip() for ln in receipt.strip().splitlines() if ln.strip()]

        expected_lines = [
            f"(==== {bun.get_name()} ====)",
            f"= sauce {sauce.get_name()} =",
            f"= filling {filling.get_name()} =",
            f"(==== {bun.get_name()} ====)",
            f"Price: {expected_price}",
        ]

        assert lines == expected_lines, f"\nОжидали:\n{expected_lines}\nПолучили:\n{lines}"