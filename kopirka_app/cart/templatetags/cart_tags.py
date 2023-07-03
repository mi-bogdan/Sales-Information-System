from cart.models import Cart, CartItem
from django import template


register=template.Library()

@register.inclusion_tag('tags/tags_cart.html',takes_context=True)
def global_cart(context):
    request = context['request']
    if request.user.is_authenticated:
        carts = Cart.objects.get(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        carts = Cart.objects.get(session_id=session_key)
    return {'carts': carts, 'lists': CartItem.objects.filter(cart=carts),'request':request}