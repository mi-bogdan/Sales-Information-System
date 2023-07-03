from django.contrib import admin
from .models import Category, Produkt, Prefix, Reviews, ImageProduct, ProductFeature, CategoryFeature
from mptt.admin import MPTTModelAdmin
from django.db import models
from django.forms import CheckboxSelectMultiple


class CategoryAdmin(MPTTModelAdmin):
    mptt_indent_field = 'title'
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title',)
    prepopulated_fields = {'slug': ('title',), }

admin.site.register(Category, CategoryAdmin)



admin.site.register(Prefix)
admin.site.register(ImageProduct)


@admin.register(Produkt)
class ProduktAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'create_at', 'update_at',
                    'category', 'published')
    list_display_links = ('id', 'title')
    prepopulated_fields = {'slug': ('title',), }


@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'value', 'show_product']
    list_display_links = ('id', 'title')
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def show_product(self, obj):
        return ",\n".join([a.title for a in obj.products.all()])


@admin.register(CategoryFeature)
class CategoryFeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'value', 'show_category')
    list_display_links = ('id', 'title')

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def show_category(self, obj):
        return ",\n".join([a.title for a in obj.categories.all()])

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'produkt','create_at')
    list_display_links = ('id', 'name')
    

