from .models import *
from .service import *


class MixinCategory():
    """Миксин для вывода дополнительной информации на страницу"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.filter(parent__isnull=True)
        context['cat'] = Category.objects.get(slug=self.kwargs['slug'])
        context['feature_category'] = display_list_dict(
            Category.objects.get(slug=self.kwargs['slug']))
        return context
