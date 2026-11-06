from decimal import Decimal
from .models import Product

class Cart:
    SESSION_KEY = "cart"

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(self.SESSION_KEY, {})

    def add(self, product, quantity=1, override=False):
        product_id = str(product.id)
        current = self.cart.get(product_id, {"quantity": 0})
        new_quantity = quantity if override else current["quantity"] + quantity
        if new_quantity < 1:
            self.remove(product)
            return
        self.cart[product_id] = {"quantity": min(new_quantity, product.stock)}
        self.save()

    def remove(self, product):
        self.cart.pop(str(product.id), None)
        self.save()

    def save(self):
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids, is_active=True)
        for product in products:
            quantity = self.cart[str(product.id)]["quantity"]
            yield {"product": product, "quantity": quantity,
                   "price": product.price, "total": product.price * quantity}

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum((item["product"].price * item["quantity"] for item in self), Decimal("0.00"))

    def clear(self):
        self.session[self.SESSION_KEY] = {}
        self.session.modified = True
