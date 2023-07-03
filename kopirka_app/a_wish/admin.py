from django.contrib import admin
from .models import A_Wish

@admin.register(A_Wish)
class AWishAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    list_display_links = ('id', 'user')
