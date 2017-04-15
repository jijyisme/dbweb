from django.http import HttpResponse
from django.shortcuts import render

from . import views
def index(request) :
    return render(request, 'index.html')

def hey(request) :
    return render(request, 'hey.html')




