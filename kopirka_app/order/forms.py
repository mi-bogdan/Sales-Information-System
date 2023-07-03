from django import forms
from .models import Order,DeliveryMethod


class OrderForms(forms.Form):
    """Форма заказа"""
    first_name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    note_order = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control','style':'height: 100px;'}))
    delivery_method = forms.ModelChoiceField(queryset=DeliveryMethod.objects.all(),
                                      widget=forms.RadioSelect(attrs={'class': ''}))

    def __init__(self, *args, **kwargs):
            if 'user' in kwargs:
                user = kwargs.pop('user')
                super().__init__(*args, **kwargs)
                self.fields['first_name'].initial = user.first_name
                self.fields['last_name'].initial = user.last_name
                self.fields['email'].initial = user.email
            else:
                super().__init__(*args, **kwargs)

    
