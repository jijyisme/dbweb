from django.http import HttpResponse
from django.shortcuts import render
import json
from . import views
def index(request) :
    return render(request, 'login.html')


def test(request) :
    return render(request, 'jstest.html')



