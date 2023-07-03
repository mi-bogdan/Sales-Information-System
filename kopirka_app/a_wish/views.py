from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import A_Wish
from shop.models import Produkt
from django.views.generic.base import View


class AddToWish(View):
    """Добавление товара в список желаний"""
    def get(self, request, product_id):
        product = get_object_or_404(Produkt, id=product_id)
        wish, created = A_Wish.objects.get_or_create(
            user=request.user, product=product)
        messages.success(request, "Product added to wish")
        return redirect('wish')


class Wish(View):
    """Страница списка желаний"""
    def get(self, request):
        wish = A_Wish.objects.filter(user=request.user)
        return render(request, 'wish/a_wish.html', {'wish': wish})


class RemoveFromWish(View):
    """Удаление списка желаний со страницы"""
    def get(self, request, item_id):
        a_wish_item = A_Wish.objects.get(id=item_id, user=request.user)
        a_wish_item.delete()
        return redirect('wish')


class RemoveFull(View):
    """Очистить список желаний"""
    def get(self, request):
        a_wish_item = A_Wish.objects.filter(user=request.user)
        for item in a_wish_item:
            item.delete()
        return redirect('wish')
