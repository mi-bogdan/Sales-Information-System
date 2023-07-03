from django.shortcuts import render, redirect
from cart.models import Cart, CartItem
from .models import Order, OrderItem, DeliveryMethod
from .forms import OrderForms

from django.views.generic.base import View
from django.shortcuts import redirect





def checkout_final(request):
    """Страница с оповещением что заказ отправлен"""
    return render(request, 'order/checkout-3.html')


class Orders(View):
    """Страница оформление заказа"""
    def get(self,request):
        delivery_method = DeliveryMethod.objects.all()
        if request.user.is_authenticated:
            form = OrderForms(user=request.user)
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)

        else:
            form = OrderForms()
            session_key = request.session.session_key
            if not session_key:
                request.session.cycle_key()
            cart = Cart.objects.get(session_id=session_key)
            cart_items = CartItem.objects.filter(cart=cart)
        return render(request, 'order/checkout-2.html', {'items': cart_items, 'cart': cart, 'form': form, 'delivery_method': delivery_method})

    def post(self,request):
        """Отпрвление заказа в систему"""
        form = OrderForms(request.POST)
        if request.user.is_authenticated:
            if form.is_valid():
                cd = form.cleaned_data
                cart = Cart.objects.get(user=request.user)
                cart_items = CartItem.objects.filter(cart=cart)
                order, created = Order.objects.get_or_create(user=request.user, status='Нов',
                    first_name=cd['first_name'],
                    last_name=cd['last_name'],
                    email=cd['email'],
                    phone=cd['phone'],
                    address=cd['address'],
                    city=cd['city'],
                    note_order=cd['note_order'],
                    total_price=cart.total_price,
                    delivery_method=cd['delivery_method']
                    )
                for item in cart_items:
                    order_item, created = OrderItem.objects.get_or_create(
                        order=order, product=item.product, quantity=item.quantity, price=item.price)
                    item.delete()
                cart.total_price = 0
                cart.save()

                return redirect('checkout_final')
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.cycle_key()
            
            if form.is_valid():
                cd = form.cleaned_data
                cart = Cart.objects.get(session_id=session_key)
                cart_items = CartItem.objects.filter(cart=cart)
                order, created = Order.objects.get_or_create(
                    session_id=session_key,
                    status='Нов',
                    first_name=cd['first_name'],
                    last_name=cd['last_name'],
                    email=cd['email'],
                    phone=cd['phone'],
                    address=['address'],
                    city=cd['city'],
                    note_order=cd['note_order'],
                    total_price=cart.total_price,
                    delivery_method=cd['delivery_method']
                    )
                for item in cart_items:
                    order_item, created = OrderItem.objects.get_or_create(
                        order=order, product=item.product, quantity=item.quantity, price=item.price)
                    item.delete()
                cart.total_price = 0
                cart.save()
                return redirect('checkout_final')

    