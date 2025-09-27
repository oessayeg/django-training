class HotBeverage:
    def __init__(self, name="hot beverage", price=0.30):
        self.name = name
        self.price = price

    def description(self):
        return "Just some hot water in a cup"

    def __str__(self):
        return (
            f"name: {self.name}\n"
            f"price: {self.price:.2f}\n"
            f"description: {self.description()}"
        )


class Coffee(HotBeverage):
    def __init__(self):
        super().__init__("coffee", 0.40)

    def description(self):
        return "A coffee, to stay awake."


class Tea(HotBeverage):
    def __init__(self):
        super().__init__("tea", 0.30)

    def description(self):
        return "Just some hot water in a cup."


class Chocolate(HotBeverage):
    def __init__(self):
        super().__init__("chocolate", 0.50)

    def description(self):
        return "Chocolate, sweet chocolate..."


class Cappuccino(HotBeverage):
    def __init__(self):
        super().__init__("cappuccino", 0.45)

    def description(self):
        return "Un po’ di Italia nella sua tazza!"
