from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.db.models import Q
from .models import Category, Produkt
from .forms import ReviewsForms, SearchForm

from .utils import *


class HomeIndex(ListView):
    """Гланая страница"""
    model = Produkt
    template_name = 'shop/index.html'
    context_object_name = 'produkt_all'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(parent__isnull=True)
        context['produkt_save_one'] = Produkt.objects.filter(
            discount=20).first()
        context['produkt_new_one'] = Produkt.objects.filter(
            prefix__title='Новинка').first()
        context['produkt_hit_one'] = Produkt.objects.filter(
            prefix__title='Хит').first()
        context['slider'] = Produkt.objects.all()[:5]
        context['produkt_new'] = Produkt.objects.filter(
            prefix__title='Новинка')

        return context


class DeteilProdukt(DetailView):
    """Страница подробная информация о товвре"""
    model = Produkt
    context_object_name = 'produkt'
    template_name = 'shop/shop-deteil.html'
    slug_field = 'slug'


class AddReviews(View):
    """Добавления отзыва"""
    def post(self, request, slug):
        print(request.POST)
        form = ReviewsForms(request.POST)
        produkt = Produkt.objects.get(slug=slug)
        if form.is_valid():
            forms = form.save(commit=False)
            if request.POST.get('perents', None):
                forms.perents_id = int(request.POST.get('perents'))
            forms.produkt = produkt
            forms.save()
        return redirect('deteil', produkt.slug)


class ProduktList(MixinCategory, ListView):
    """Каталог товаров"""
    model = Produkt
    template_name = 'shop/shop-list.html'
    context_object_name = 'produkt'

    def get_queryset(self):
        return Produkt.objects.filter(category__slug=self.kwargs['slug'],published=True)


class FiltersProduktView(MixinCategory, ListView):
    """Фильтрация товара"""
    model = Produkt
    template_name = 'shop/shop-list.html'
    context_object_name = 'produkt'

    def get_queryset(self):
        return Produkt.objects.filter(feature_prod__value__in=self.request.GET.getlist('feature'),published=True)


class SearchView(View):
    """Поиск товара по названию и артикулу"""
    def get(self, request):
        products = []
        query = request.GET.get('query')
        if query:
            products = Produkt.objects.filter(
                Q(title__icontains=query) | Q(sku__icontains=query)
            )

        context = {
            'products': products,
            'category': Category.objects.filter(parent__isnull=True)
        }
        return render(request, 'shop/shop-search.html', context)

class Less(MixinCategory, ListView):
    """Фильтрация по цене от меньшего"""
    model = Produkt
    template_name = 'shop/shop-list.html'
    context_object_name = 'produkt'

    def get_queryset(self):
        return Produkt.objects.filter(category__slug=self.kwargs['slug']).order_by('price')


class More(MixinCategory, ListView):
    """Фильтрация по цене от большего"""
    model = Produkt
    template_name = 'shop/shop-list.html'
    context_object_name = 'produkt'

    def get_queryset(self):
        return Produkt.objects.filter(category__slug=self.kwargs['slug']).order_by('-price')
