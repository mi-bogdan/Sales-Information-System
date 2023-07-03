from .models import *


class Prefix_get:
    def get_one(self):
        return Prefix.objects.all()[-1]

    def get_two(self):
        return Prefix.objects.all()[-2]

    def get_three(self):
        return Prefix.objects.all()[-3]


def display_list_dict(category):
    """Вывод характеристики к категории"""
    featyre = CategoryFeature.objects.filter(categories__title=category)
    new_dict = {}
    for item in featyre:
        if not item.title in new_dict:
            new_dict[item.title] = [item.value]
        else:
            new_dict[item.title].append(item.value)

    return new_dict








