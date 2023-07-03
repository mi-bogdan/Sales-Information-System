from django.test import TestCase
from django.urls import reverse

from authentications.forms import RegisterForm, LoginForms
from django.contrib.auth.models import User


class TestRegisterView(TestCase):
    """Тестирование view регистрации пользователя"""

    def test_get(self):
        """Получение формы регистрации"""
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)

    def test_post(self):
        """Тестирование на создания пользователя"""

        email = 'test_email@mail.ru'
        payload = {
            'username': 'admin',
            'email': email,
            'password': 'admin1234'
        }
        response = self.client.post(reverse('register'), data=payload)

        user = User.objects.get(email=email)

        self.assertEqual(user.email, email)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(user.is_authenticated)


class TestLoginUserView(TestCase):
    """Тестирование view авторизации пользователя"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser1', email='testemail@mail.ru', password='test123test123')

    def test_get(self):
        """Получение формы авторизации"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        """Тестирование на вход в систему"""
        get_user = User.objects.get(id=self.user.id)

        payload = {
            'username': 'testuser1',
            'password': 'test123test123'
        }

        response = self.client.post(reverse('login'), data=payload)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user.is_authenticated)


