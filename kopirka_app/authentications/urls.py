from django.urls import path
from .views import *


urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),

    path('personal_account/', PersonalAccount.as_view(), name='personal_account'),
    path('order_history/', OrderHistori.as_view(), name='order_history'),
    path('person_data/', PersonData.as_view(), name='person_data'),
    path('person_update/', PersonUpdate.as_view(), name='person_update'),
    path('password_update/', password_update, name='password_update'),

    
]
