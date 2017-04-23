from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from . import views
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def index(request):
    return render(request, "login.html")

def validate(request):
    id = request.GET.get('id', None)
    password = request.GET.get('password', None)
    type = ""

    # check if id & password match head-officer
        ## join manage_dept & professor
    manage_dept = Manage_dept.objects.select_related('d', 'p')
    for head in manage_dept:
        if id == head.p.p_id and password == head.p.p_password:
            type = "head"
    # check if id & password match professor
        else :
            teacher = Professor.objects.filter(p_id=id).filter(p_password=password)
            if (teacher):
                type = "teacher"
    # check if id & password match officer
    officer = Officer.objects.filter(o_id = id).filter(o_password = password)
    if (officer):
        type = "officer"

    data = {
        'type' : type
    }

    return JsonResponse(data)


def query(request):
    columns = request.GET.get('selected_column', None)
    filter = request.GET.get('filter', None)
    tab = request.GET.get('tab', None)

    # join student + activity table

    query = 'SELECT * FROM app_activity'
    all_persons = Activity.objects.raw(query)
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