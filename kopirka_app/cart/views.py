from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from django.contrib import messages
from .models import Cart, CartItem
from shop.models import Produkt
from django.views.generic.base import View
from django.db.models import Sum


def _cart_id(request):
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart = Cart.objects.filter(session_id=session_key).first()
        if cart is None:
            cart = Cart.objects.create(session_id=session_key)
    return cart.id


class AddToCart(View):
    """Класс добавление товара в корзину авторизованных пользователей"""

    def get(self, request, product_id):
        product = get_object_or_404(Produkt, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        if product.discount:
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, price=product.get_sale())
        else:
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, price=product.price)
        cart_item.quantity += 1
        cart_item.save()
        cart.total_price = CartItem.objects.filter(
            cart=cart).aggregate(Sum('price')).get('price__sum')
        cart.save()
        messages.success(request, "Товар добавлен в корзину")
        return redirect('cart')


class Carts(View):
    """Страница корзины авторизованых пользователей"""

    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        return render(request, 'cart/checkout-1.html', {'items': cart_items, 'cart': cart})


class RemoveFromCart(View):
    """Удаление товара с корзины авторизованных пользователей"""

    def get(self, request, item_id):
        cart_item = get_object_or_404(
            CartItem, id=item_id, cart__user=request.user)
        cart = cart_item.cart
        cart_item.delete()
        cart.total_price = CartItem.objects.filter(
            cart=cart).aggregate(Sum('price')).get('price__sum')
        cart.save()
        messages.success(request, "Товар удален с корзины")
        return redirect('cart')


class AddToCartAnonym(View):
    """Добавление товара в корзину не авторизованых пользователей"""

    def get(self, request, product_id):
        product = get_object_or_404(Produkt, id=product_id)
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart = Cart.objects.filter(session_id=session_key).first()
        if cart is None:
            cart = Cart.objects.create(session_id=session_key)
        if product.discount:
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, price=product.get_sale())
        else:
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, price=product.price)
        cart_item.quantity += 1
        cart_item.save()
        cart.total_price = CartItem.objects.filter(
            cart=cart).aggregate(Sum('price')).get('price__sum')
        cart.save()
        messages.success(request, "Product added to cart")
        return redirect('cart_anonim')


class CartAnonym(View):
    """Страница корзины не авторизованных пользователей"""

    def get(self, request):
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart = Cart.objects.filter(session_id=session_key).first()
        cart_items = CartItem.objects.filter(cart=cart)
        return render(request, 'cart/checkout-1.html', {'items': cart_items, 'cart': cart})


class RemoveFromCartAnonym(View):
    """Удаление товара с корзины для не авторизованных пользователей"""

    def get(self, request, item_id):
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart = Cart.objects.filter(session_id=session_key).first()
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        cart_item.delete()
        cart.total_price = CartItem.objects.filter(
            cart=cart).aggregate(Sum('price')).get('price__sum')
        cart.save()
        messages.success(request, "Product removed from cart")
        return redirect('cart_anonim')


def add_quantity(request, id):
    """Добавить кол-во товара для заказа для всех пользователей"""
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        item = CartItem.objects.get(pk=id, cart=cart)
        item.quantity += 1

        if item.product.discount:
            item.price = item.quantity * item.product.get_sale()
        else:
            item.price = item.quantity * item.product.price
        item.save()
        cart.total_price = CartItem.objects.filter(
            cart=cart).aggregate(Sum('price')).get('price__sum')
        cart.save()
        return redirect('cart')
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart = Cart.objects.get(session_id=session_key)
        item = CartItem.objects.get(pk=id, cart=cart)
        item.quantity += 1

        if item.product.discount:
            item.price = item.quantity * item.product.get_sale()

        else:
            item.price = item.quantity * item.product.price
        item.save()
        cart.total_price = CartItem.objects.filter(
            cart=cart).aggregate(Sum('price')).get('price__sum')
        cart.save()
        return redirect('cart_anonim')


def clean_up_quantity(request, id):
    """Уменьшить кол-во товара для заказа для всех пользователей"""
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        item = CartItem.objects.get(
            pk=id, cart=cart)
        if item.quantity <= 1:
            item.quantity = 1
        else:
            item.quantity -= 1
        if item.product.discount:
            item.price = item.quantity * item.product.get_sale()
        else:
            item.price = item.quantity * item.product.price

        item.save()
        cart.total_price = CartItem.objects.filter(
            cart=cart).aggregate(Sum('price')).get('price__sum')
        cart.save()
        return redirect('cart')
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart = Cart.objects.get(session_id=session_key)

        item = CartItem.objects.get(
            pk=id, cart=cart)
        if item.quantity <= 1:
            item.quantity = 1
        else:
            item.quantity -= 1
        if item.product.discount:
            item.price = item.quantity * item.product.get_sale()
        else:
            item.price = item.quantity * item.product.price
        item.save()
        cart.total_price = CartItem.objects.filter(
            cart=cart).aggregate(Sum('price')).get('price__sum')
        cart.save()
        return redirect('cart_anonim')
