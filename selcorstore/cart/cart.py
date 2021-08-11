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

    def remove(self, product):
        """
        Removing product from the cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Iteration through elements of the cart and uploading products from database
        """
        product_ids = self.cart.keys()
        # uploading product objects and adding them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
            for item in cart.values():
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        """
        Counting all elements in the cart
        """
        return sum(item['quantity'] for item in self.cart.values())

    # Method for counting all elements in the cart
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # removing cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()