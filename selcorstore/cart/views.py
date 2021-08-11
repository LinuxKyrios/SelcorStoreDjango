from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from selcorshop.models import Product
from .cart import Cart
from .forms import CartAddProductForm


# View for adding items to the cart or updating quantity
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=['update'])
    return redirect('cart:cart_detail')


# View for removing items from cart
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


# View for display products in cart
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'override': True}
        )
    return render(request, 'cart/detail.html', {'cart': cart})