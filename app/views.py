from django.http import HttpResponse
from django.shortcuts import render
#from .models import Person
from . import views
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, "login.html")

def validate(request):
    first_name = request.GET.get('first_name', None)

    query = 'SELECT * FROM sql_person'
#    all_persons = Person.objects.raw(query)
    selected_columns = ['first_name', 'last_name']
    data = {}
    for column in selected_columns:
        data[column] = []

    for person in all_persons:
        for column in selected_columns:
            if column == 'first_name':
                data[column].append(person.first_name)
            elif column == 'last_name':
                data[column].append(person.last_name)

    return JsonResponse(data)
## for test jijy's sctipt
def validate_copy(request):
    return HttpResponse("teacher")


def teacher(request) :
    return render(request, 'teacher.html')
def head(request) :
    return render(request, 'head.html')
def officer(request) :
    return render(request, 'officer.html')