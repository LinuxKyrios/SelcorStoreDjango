from decimal import Decimal
from django.conf import settings
from selcorshop.models import Product


class Cart(object):
    def __init__(self, request):
        """
        Shop cart initialization
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Saving empty shop cart
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product,quantity=1, update_quantity=False):
        """
        Adding product to cart or change it
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product.id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True