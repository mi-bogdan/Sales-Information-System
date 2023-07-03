from django.urls import path


from .views import Wish, AddToWish, RemoveFromWish, RemoveFull

urlpatterns = [
    path('add_wish/<int:product_id>/', AddToWish.as_view(), name='add_to_wish'),
    path('', Wish.as_view(), name='wish'),
    path('remove_wish/<int:item_id>/',RemoveFromWish.as_view(), name='remove_from_wish'),
    path('remove_wish_full/', RemoveFull.as_view(), name='remove_full'),
]
