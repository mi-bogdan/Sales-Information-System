from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
    path('auth/', include('authentications.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('wish/', include('a_wish.urls')),
    path('contact/', include('contact.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
