class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    """Метод для проверки количества продуктов"""
    def check_quantity(self, quantity) -> bool:
        if self.quantity >= quantity:
            return True
        else:
            return False

    """Метод покупки"""
    def buy(self, quantity):
        if self.check_quantity(quantity):
            self.quantity -= quantity
        else:
            raise ValueError("Недостаточно продуктов")

    """Метод для возврата хеша продукта по его наименованию и описанию"""
    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """Класс корзины. В нем хранятся продукты, которые пользователь хочет купить."""

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество"""
        if product in self.products:
            self.products[product] += buy_count
        else:
            self.products[product] = buy_count

    def remove_product(self, product: Product, remove_count=None):
        """Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция"""
        if product in self.products:
            if remove_count is None or self.products[product] <= remove_count:
                del self.products[product]
            else:
                self.products[product] -= remove_count

    """Метод для очистки корзины"""
    def clear(self):
        self.products.clear()

    """Метод для расчета стоимости всех товаров в корзине"""
    def get_total_price(self) -> float:
        total_price = 0.0
        for product, count in self.products.items():
            total_price += product.price * count
        return total_price

    def buy(self):
        """Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError"""
        for product, quantity in self.products.items():
            product.buy(quantity)
        self.clear()

