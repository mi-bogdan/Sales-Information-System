from django.shortcuts import render,redirect
from .models import Contact
from .forms import ContactForms
from django.views.generic.base import View

class AddContact(View):
    """Добавить почту для новостей"""
    def post(self, request):
        form = ContactForms(request.POST)
        if form.is_valid():
            form.save()
        return redirect("index")