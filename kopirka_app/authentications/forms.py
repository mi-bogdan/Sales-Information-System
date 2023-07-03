from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class LoginForms(forms.Form):
    """Форма авторизации"""
    username = forms.CharField()
    password = forms.CharField()

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        password = cleaned_data['password']
        try:
            self.user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('Не верный логин')
        if not self.user.check_password(password):
            raise forms.ValidationError('Пароль не верный ')


class RegisterForm(forms.ModelForm):
    """Форма регистрации"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class FormUpdate(forms.ModelForm):
    """Форма обновление данных пользователя в личном кабинете"""
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ChangePasswordForm(PasswordChangeForm):
    """Форма замена старого пароля на новый"""
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(label='Повторите', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
