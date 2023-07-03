from django.urls import path
from .views import AddContact


urlpatterns = [
   path('', AddContact.as_view(), name='contact'),
]