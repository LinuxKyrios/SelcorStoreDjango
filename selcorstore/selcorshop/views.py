from django.shortcuts import render, get_object_or_404
from .models import Category, Subcategory, Product
from cart.forms import CartAddProductForm


# View for product list in site
def product_list(request, category_slug=None, subcategory_slug=None):
    category = None
    categories = Category.objects.all()
    subcategory = None
    subcategories = Subcategory.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        subcategory = get_object_or_404(Subcategory, slug=subcategory_slug)
        products = products.filter(category=category)
    return render(request,
                  'selcorshop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'subcategory': subcategory,
                   'subcategories': subcategories,
                   'products': products})


# View for single product
def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id = id,
                                slug = slug,
                                available = True)
    # Add to cart button
    cart_product_form = CartAddProductForm()
    return render(request,
                  'selcorshop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})