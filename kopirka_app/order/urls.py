from django.urls import path, include
from .views import Orders,checkout_final

urlpatterns = [
   path('', Orders.as_view(), name='order'),
   path('final/', checkout_final, name='checkout_final'),
   
]