from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from .forms import LoginForms, RegisterForm, FormUpdate, ChangePasswordForm
from django.views.generic import TemplateView
from shop.models import Category
from django.contrib.auth.models import User
from order.models import Order

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View


class LoginUser(View):
    def post(self, request):
        login_form = LoginForms(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')

    def get(self, request):
        context = {'login_forms': LoginForms()}
        return render(request, 'auth/login.html', context)


class RegisterUser(TemplateView):
    """Регистрация"""
    template_name = 'auth/register.html'

    def post(self, request):
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('index')


def logout_user(request):
    """Выход с системы"""
    logout(request)
    return redirect('index')


class PersonalAccount(View):
    """Личный кабинет пользователя"""
    def get(self, request):
        context = {
            'category': Category.objects.filter(parent__isnull=True)
        }
        return render(request, 'auth/personal_account.html', context)


class OrderHistori(View):
    """Страница истории заказов пользователя"""
    def get(self, request):
        order = Order.objects.filter(user=request.user).order_by('-pk')
        context = {
            'category': Category.objects.filter(parent__isnull=True),
            'order': order,
        }
        return render(request, 'auth/order_history.html', context)


class PersonData(View):
    """Страница персональных данных пользователя"""
    def get(self, request):
        user = User.objects.get(id=request.user.id)

        context = {
            'category': Category.objects.filter(parent__isnull=True),
            'user': user,
        }
        return render(request, 'auth/person_data.html', context)


class PersonUpdate(View):
    """Обновление персональных данных пользователя"""
    def get(self, request):
        context = {
            'category': Category.objects.filter(parent__isnull=True),
        }
        return render(request, 'auth/person_data.html', context)

    def post(self, request):
        obj = User.objects.get(id=request.user.id)
        form = FormUpdate(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('person_data')



@login_required
def password_update(request):
    """Изменение пароля пользователя"""
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('password_update')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибку ниже.')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'auth/password_update.html', {'form': form, 'category': Category.objects.filter(parent__isnull=True)})


# def password_update(request):
#     user = User.objects.get(id=request.user.id)

#     context = {
#         'category': Category.objects.filter(parent__isnull=True),
#         'user': user,
#     }
#     return render(request, 'auth/person_data.html', context)