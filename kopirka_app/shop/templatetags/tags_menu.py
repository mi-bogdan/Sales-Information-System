from shop.models import Category
from django import template


register=template.Library()

@register.inclusion_tag('tags/tags_menu.html')
def menu():
    category= Category.objects.filter(parent__isnull=True)
    return {'category': category}