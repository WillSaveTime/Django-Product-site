from django.http import request
from django.shortcuts import render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.http import Http404  
from django.views.generic import View

from .models import Pyme, PymeUser
from django.contrib.auth.models import User
from . import models


def select_pyme_view(request: HttpRequest) -> HttpResponse:
    pymes = Pyme.objects.active().filter(users__user=request.user)
    pymes_count = pymes.count()
    context = {
        'pymes': pymes,
    }

    if pymes_count < 1:
        return HttpResponse('User has no Pymes', status=404)

    elif pymes_count > 1:
        return render(request, "pymes/pyme-select/pyme-select.html", context)

    else:
        pyme_code = pymes.first().code
        return redirect('dashboard-home', pyme_code=pyme_code)


class PymeAuthView(View):
    def dispatch(self, request: HttpRequest, pyme_code:str=None, *args, **kwargs):
        try:
            self.pyme = Pyme.objects.active().get(code=pyme_code)
            self.pyme_user = self.pyme.users.active().get(user=request.user)
        except:
            return HttpResponse('Unauthorized', status=401)

        return super(PymeAuthView, self).dispatch(request, *args, **kwargs)


class DashboardHomeView(PymeAuthView):
    def get(self, request: HttpRequest, pyme_code:str=None, *args, **kwargs) -> HttpResponse:
        context = {
            'pyme': self.pyme,
        }
        return render(request, "dashboard/home/home.html", context)



