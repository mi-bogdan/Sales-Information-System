from django.urls import path


from .views import AddToCart, Carts, RemoveFromCart, AddToCartAnonym, CartAnonym, RemoveFromCartAnonym, add_quantity, clean_up_quantity

urlpatterns = [
    path('add/<int:product_id>/', AddToCart.as_view(), name='cart_add'),
    path('', Carts.as_view(), name='cart'),
    path('remove/<int:item_id>/', RemoveFromCart.as_view(), name='cart_remove'),

    path('anonim/add/<int:product_id>/', AddToCartAnonym.as_view(), name='cart_add_anonim'),
    path('anonim/', CartAnonym.as_view(), name='cart_anonim'),
    path('anonim/remove/<int:item_id>/',RemoveFromCartAnonym.as_view(), name='cart_remove_anonim'),

    path('add_quantity/<int:id>/', add_quantity, name='add_quantity'),
    path('clean_up_quantity/<int:id>/',
         clean_up_quantity, name='clean_up_quantity'),


]
