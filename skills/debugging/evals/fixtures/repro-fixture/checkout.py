TAX_RATE = 0.10


class Cart:
    def __init__(self):
        self._items = []

    def add_item(self, name, price, quantity=1):
        self._items.append((price, quantity))

    def subtotal(self):
        return sum(price * quantity for price, quantity in self._items)

    def total(self, discount=0.0):
        subtotal = self.subtotal()
        discounted = subtotal * (1 - discount)
        tax = discounted * TAX_RATE
        return round(discounted + tax, 2)
