import pytest
from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


class TestProducts:
    """Проверки на метод check_quantity"""

    def test_product_check_quantity(self, product):
        # Проверка на получение продуктов < доступного количества
        assert product.check_quantity(product.quantity - 1)
        # Проверка на получение продуктов = доступному количеству
        assert product.check_quantity(product.quantity)
        # Проверка на получение продуктов > доступного количества
        assert not product.check_quantity(product.quantity + 1)

    """Проверки на метод buy"""

    def test_product_buy(self, product):
        # Проверка покупки продуктов < доступного количества
        available_quantity = product.quantity
        quantity = product.quantity - 1
        product.buy(quantity)
        assert product.quantity == available_quantity - quantity

        # Проверка покупки продуктов = доступному количеству
        available_quantity = product.quantity
        quantity = product.quantity
        product.buy(quantity)
        assert product.quantity == available_quantity - quantity

    def test_product_buy_more_than_available(self, product):
        # Проверка покупки продуктов > доступного количества
        available_quantity = product.quantity
        quantity = product.quantity + 1
        with pytest.raises(ValueError) as e:
            product.buy(quantity)
        assert product.quantity == available_quantity and "Недостаточно продуктов" in str(e.value)


class TestCart:

    @pytest.fixture
    def cart(self):
        return Cart()

    """Проверки на метод add_product"""

    def test_add_product_empty_cart(self, product, cart):
        # Проверка добавления продукта в пустую корзину
        cart.add_product(product, 1)
        assert cart.products[product] == 1

    def test_add_product_not_empty_cart(self, product, cart):
        # Проверка добавления продуктов в наполненную корзину
        cart.add_product(product, 1)
        cart.add_product(product, 4)
        assert cart.products[product] == 5

    """Проверки на метод remove_product"""

    def test_remove_product_all(self, product, cart):
        # Проверка удаления без указания количества
        cart.add_product(product, 1000)
        cart.remove_product(product)
        assert product not in cart.products

    def test_remove_product_fully_cart(self, product, cart):
        # Проверка удаления количества = количеству в корзине
        cart.add_product(product, 5)
        cart.remove_product(product, 5)
        assert product not in cart.products

    def test_remove_product_partly(self, product, cart):
        # Проверка частичного удаления продуктов из корзины
        cart.add_product(product, 5)
        cart.remove_product(product, 2)
        assert cart.products[product] == 3

    def test_remove_product_fully_stock(self, product, cart):
        # Проверка удаления количества = количеству на складе
        cart.add_product(product, 1000)
        cart.remove_product(product, 1000)
        assert product not in cart.products

    def test_remove_product_more_than_available(self, product, cart):
        # Проверка удаления количества > количество на складе
        cart.add_product(product, 1000)
        cart.remove_product(product, 1001)
        assert product not in cart.products

    def test_clear(self, product, cart):
        # Проверка очистки корзины
        cart.add_product(product, 5)
        cart.clear()
        assert product not in cart.products

    """Проверки на метод get_total_price"""

    def test_get_total_price(self, product, cart):
        # Проверка расчета стоимости всех товаров в корзине
        cart.add_product(product, 5)
        cart.add_product(product, 2)
        assert cart.get_total_price() == product.price * 5 + product.price * 2

        """Проверки на метод buy"""

    def test_cart_buy_success(self, product, cart):
        # Проверка успешной покупки товаров из корзины
        cart = Cart()
        product = Product("Томаты", 10, 'Красные', 200)

        cart.add_product(product, 2)
        cart.buy()

        assert product.quantity == 198
        assert product not in cart.products

    def test_cart_buy_error(self, product, cart):
        # Проверка получения ошибки при покупке товаров
        cart = Cart()
        product = Product("Томаты", 10, 'Красные', 200)
        cart.add_product(product, 202)
        with pytest.raises(ValueError) as exception:
            cart.buy()

        assert exception.typename == 'ValueError' and product.quantity == 200
