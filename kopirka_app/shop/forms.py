from django import forms
from .models import Reviews


class ReviewsForms(forms.ModelForm):
    """Форма отзыва"""
    class Meta:
        model = Reviews
        fields = ['text', 'name', 'email']


class SearchForm(forms.Form):
    """Форма поиска товара"""
    query = forms.CharField(max_length=100, label='Search')