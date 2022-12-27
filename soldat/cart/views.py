from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from app.models import Products
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib import messages


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, product_id=product_id)
    print(type(product))
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        quan = get_object_or_404(Products, product_id=product_id).quantity
        if cd['quantity'] not in range(1, quan):
            if cd['quantity'] < 0 :
                messages.error(request, f'Amount must be positive')
                return redirect(to='/')
            messages.error(request, f'There are only {quan} items of this product')
            return redirect(to='/')
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Products, product_id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})