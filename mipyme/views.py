import django
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import View

from mipyme.forms import LoginForm
from pymes.models import Pyme, PymeUser


def home_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'landing/home.html')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('select-pyme')
        else:
            return render(request, 'landing/login/login.html')

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            user = authenticate(username= username, password= password)
            if user is not None:
                login(request, user)
                return redirect('select-pyme')

            else:
                messages.error(request,'Usuario o contraseña incorrectos!')
                return redirect('login')

        else:
            print("not valid")

        return render(request, 'login/login.html')


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("home")