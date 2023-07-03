
from django.urls import path
from .views import HomeIndex, DeteilProdukt, AddReviews, ProduktList, FiltersProduktView,SearchView,Less,More

urlpatterns = [
    path('', HomeIndex.as_view(), name='index'),
    path('deteil/<slug>/', DeteilProdukt.as_view(), name='deteil'),
    path('reviews/<slug>/', AddReviews.as_view(), name='reviews'),
    path('list/<slug>/', ProduktList.as_view(), name='list'),
    path('filter/<slug>/', FiltersProduktView.as_view(), name='filter'),
    path('search_view/', SearchView.as_view(), name='search_view'),
    path('less/<slug>/', Less.as_view(), name='less'),
    path('more/<slug>/', More.as_view(), name='more'),

]
