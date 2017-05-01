from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import json
import ast
import datetime

from . import views
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

# static variable for id whose log in.
## type = "officer" or "head" or "teacher"
class Person:
    id = "",
    type = ""
class Current:
    year = datetime.datetime.now().year
    term = "8"

# Create your views here.
def index(request):
    return render(request, "login.html")

def validate(request):
    # 210101 officer
    # 31300421 head
    # 38311121 teacher
    id = request.GET.get('id', None)
    password = request.GET.get('password', None)
    type = ""

    # check if id & password match head-officer
        ## join manage_dept & professor
    manage_dept = Manage_dept.objects.select_related('d', 'p')
    is_head_exist = False
    for head in manage_dept:
        if id == head.p.p_id and password == head.p.p_password:
            type = "head"
            is_head_exist = True
    # check if id & password match professor
    if not is_head_exist:
        teacher = Professor.objects.filter(p_id=id).filter(p_password=password)
        if (teacher):
            type = "teacher"
    # check if id & password match officer
    officer = Officer.objects.filter(o_id = id).filter(o_password = password)
    if (officer):
        type = "officer"

    data = {
        'type' : type,
    }

    # assign static value by logging in
    Person.id = id
    Person.type = type
    print(data)
    return JsonResponse(data)


# def query(request):
#     type = 'officer'
#
#     # Receiving object from ajax

def query(request):

    lists = request.POST.items()

    for i in lists:
        dict = ast.literal_eval(i[0])
    print(dict['tab'], dict['filter'])

    filters = dict['filter']
    tab = dict['tab']

    selected_columns = []
    for filter in filters:
        selected_columns.append(filter[0])
    print(selected_columns)
    # [["id", ">", "1"]]

    query = {
        'officer' : {
            'tab_student' :
                '''
                SELECT * FROM app_student S
                JOIN app_department ON app_department.d_id = S.d_id
                JOIN app_faculty ON app_faculty.f_id = app_department.f_id
                JOIN app_supervise ON app_supervise.s_id = S.s_id
                JOIN app_professor ON app_professor.p_id = app_supervise.p_id
                ''',
            'tab_teacher':
                '''
                SELECT * FROM app_professor P
                JOIN app_department ON app_department.d_id = P.d_id
                JOIN app_faculty ON app_faculty.f_id = app_department.f_id
                ''',
            'tab_scholarship':
                '''
                SELECT * FROM app_student S
                JOIN app_get_scholarship ON app_get_scholarship.s_id = S.s_id 
                JOIN app_scholarship ON app_scholarship.sch_id = app_get_scholarship.sch_id
                JOIN app_semester ON app_semester.id = app_get_scholarship.term_year_id;
                ''',
        },
        'teacher' : {
            'tab_enroll' :
                '''
                SELECT * FROM app_enrollment Enroll, app_student S, app_course C
                WHERE S.s_id = Enroll.s_id AND C.c_id = Enroll.c_id
                AND S.s_id IN (SELECT S.s_id FROM app_student S, app_professor P, app_supervise Supervise
                WHERE S.s_id = Supervise.s_id AND P.p_id = Supervise.p_id AND P.p_id = %s);
                ''',
            'tab_student' :
                '''
                SELECT * FROM app_student S, app_professor P, app_supervise Supervise
                WHERE S.s_id = Supervise.s_id AND P.p_id = Supervise.p_id AND P.p_id = %s
                ''',
        },
        'head' : {

        }
    }

    # --------------- Deal with filter condition ---------------

    filter_exist = False
    where = ""
    values = [Person.id] if (Person.type == 'teacher') else []

    for filter in filters:
        column = filter[0]
        op = filter[1]
        value = filter[2]
        if (op and value):
            if (column == 's_year'): column = "since"
            where = where + " AND " + column + " " + op + " %s"
            print("------" + where)
            values.append(value)

    if (where):
        filter_exist = True
        if (not Person.type == 'teacher'):
            where = where[4:]
            where = "WHERE S." + where

    # --------------- Start querying object ---------------

    print("filter_exist = ", filter_exist)
    print(query[Person.type][tab])
    print(where)
    print(values)

    if (tab in ["tab_teacher", "tab_dean"] and Person.type == 'officer'):
        if (filter_exist):
            all_results = Professor.objects.raw(query[Person.type][tab] + where, values)
        else:
            print("t")
            all_results = Professor.objects.raw(query[Person.type][tab])
    else:
        if (filter_exist):
            print(query[Person.type][tab] + where)
            print(values)
            all_results = Student.objects.raw(query[Person.type][tab] + where, values)
        else:
            print("o")
            all_results = Student.objects.raw(query[Person.type][tab])

    data = {
        'column' : []
    }
    for column in selected_columns:
        data['column'].append(column)
        data[column] = []
    for result in all_results:
        for column in selected_columns:
            if column == 's_id':
                data[column].append(result.s_id)
            elif column == 's_name':
                data[column].append(result.s_name)
            elif column == 's_surname':
                data[column].append(result.s_surname)
            elif column == 's_department':
                data[column].append(result.d_name)
            elif column == 's_faculty':
                data[column].append(result.f_name)
            elif column == 's_address':
                data[column].append(result.s_address)
            elif column == 's_tel':
                data[column].append(result.s_tel_no)
            elif column == 's_year':
                year = Current.year - result.since
                data[column].append(result.since)
            elif column == 'p_name':
                data[column].append(result.p_name)
            elif column == 'p_id':
                data[column].append(result.p_id)
            elif column == 'p_surname':
                data[column].append(result.p_surname)
            elif column == 'p_department':
                data[column].append(result.d_name)
            elif column == 'p_faculty':
                data[column].append(result.f_name)
            elif column == 'p_address':
                data[column].append(result.p_address)
            elif column == 'p_tel':
                data[column].append(result.p_tel)
            elif column == 'p_email':
                data[column].append(result.p_email)

    print(data)
    return JsonResponse(data)

def user_info(request):

    query = {
        'officer' : '''
            SELECT * FROM app_officer O
            JOIN app_department ON app_department.d_id = O.d_id
            WHERE O.o_id = %s;
        ''',
        'teacher_dean' : '''
            SELECT * FROM app_professor P
            JOIN app_manage_faculty ON app_manage_faculty.p_id = P.p_id
            JOIN app_faculty ON app_manage_faculty.f_id = app_faculty.f_id
            WHERE P.p_id = %s;
        ''',
        'teacher': '''
            SELECT * FROM app_professor P
            JOIN app_department ON app_manage_dept.d_id = P.d_id
            JOIN app_faculty ON app_department.f_id = app_faculty.f_id
            WHERE P.p_id = %s;
        ''',
        'teacher_head' : '''
            SELECT * FROM app_professor P
            JOIN app_manage_dept ON app_manage_dept.p_id = P.p_id
            JOIN app_department ON app_manage_dept.d_id = app_department.d_id            
            WHERE P.p_id = %s;
        '''
    }
    # type = 'officer'
    data = {
        'name' : "",
        'position' : "",
        'department' : "",
        'faculty' : ""
    }

    if (Person.type == 'teacher'):
        for result in Professor.objects.raw(query['teacher'], [Person.id]):
            data['name'] = result.p_title + " " + result.p_name + " " + result.p_surname
            data['position'] = "Professor"
            data['department'] = result.d_name
            data['faculty'] = result.f_name

        for result in Professor.objects.raw(query['teacher_dean'], [Person.id]):
            if (result):
                data['name'] = result.p_title + " " + result.p_name + " " + result.p_surname
                data['position'] = "Dean"
                data['department'] = result.d_name
                data['faculty'] = result.f_name
    elif (Person.type == 'head'):
        for result in Professor.objects.raw(query['teacher_head'], [Person.id]):
            data['name'] = result.p_title + " " + result.p_name + " " + result.p_surname
            data['position'] = "Head of department"
            data['department'] = result.d_name
            data['faculty'] = result.f_name

    else:
        for result in Officer.objects.raw(query[Person.type], [Person.id]):
            data['name'] = result.o_title + " " + result.o_name + " " + result.o_surname
            data['position'] = "Officer"
            data['department'] = "-"
            # data['faculty'] = result.f_name
    print(data)
    return JsonResponse(data)



def student_info(request):
    s_id = request.POST.get('id', None)
    print("##################")
    print(s_id)
    query = {
        'info' : '''
            SELECT * FROM app_student S
            JOIN app_department ON app_department.d_id = S.d_id
            JOIN app_faculty ON app_faculty.f_id = app_department.f_id
            WHERE S.s_id = %s;
        ''',
        'acivity' : '''
            SELECT * FROM app_student S
            JOIN app_activity_participation ON app_activity_participation.s_id = S.s_id
            JOIN app_activity ON app_activity_participation.a_id = app_activity.a_id
            WHERE S.s_id = %s;
        ''',
        'enroll' : '''
            SELECT * FROM app_student S
            JOIN app_enrollment ON app_enrollment.s_id = S.s_id
            JOIN app_course ON app_enrollment.c_id = app_course.c_id
            JOIN app_semester ON app_semester.id = app_enrollment.term_year_id
            WHERE S.s_id = %s;
        ''',
        'intern' : '''
            SELECT * FROM app_student S
            JOIN app_interns ON app_interns.s_id = S.s_id
            JOIN app_company ON app_company.comp_id = app_interns.comp_id
            WHERE S.s_id = %s;
        ''',
        'exchange' : '''
            SELECT * FROM app_student S
            JOIN app_take_exchange_program ON app_take_exchange_program.s_id = S.s_id
            JOIN app_exchange_program ON app_exchange_program.ex_id = app_take_exchange_program.ex_id
            JOIN app_semester ON app_semester.id = app_take_exchange_program.term_year_id
            WHERE S.s_id = %s;
        ''',
        'senior_project' : '''
            SELECT * FROM app_student S
            JOIN app_senior_project ON app_senior_project.s_id = S.s_id
            JOIN app_project ON app_project.project_id = app_senior_project.project_id
            JOIN app_professor ON app_project.p_id = app_professor.p_id
            WHERE S.s_id = %s;
        ''',
        'thesis': '''
            SELECT * FROM app_student S
            JOIN app_thesis ON app_thesis.s_id = S.s_id
            JOIN app_project ON app_project.project_id = app_thesis.project_id
            JOIN app_professor ON app_project.p_id = app_professor.p_id
            WHERE S.s_id = %s;
        ''',
        'status': '''
                SELECT * FROM app_student S
                JOIN app_status ON app_status.s_id = S.s_id
                WHERE S.s_id = %s AND app_status.term_year_id = %s;
        ''',
        'scholarship': '''
            SELECT * FROM app_student S
            JOIN app_get_scholarship ON app_get_scholarship.s_id = S.s_id 
            JOIN app_scholarship ON app_scholarship.sch_id = app_get_scholarship.sch_id
            JOIN app_semester ON app_semester.id = app_get_scholarship.term_year_id
            WHERE S.s_id = %s
        '''
    }

    student_id = s_id
    # student_id = "5730000621"
    # $("#pd_year").append(data['name']);
    data = {
        'id' : student_id,
        'year': 0,
        's_name' : "-",
        'department' : "-",
        'faculty' : "-",
        'tel_no' : "-",
        'email' : "-",
        'address' : "-",
        'gpax' : 0,
        'student_status' : "-",
        'drop_status' : "-",
        'activity' : [],
        'comp_name' : "-",
        'exchange' : "-",
        'project_name' : "-",
        'project_field': "-",
        'project_advisor': "-",
        'project_type': "-",
        'scholarship': "-",
        'enroll': [],
        'comp_name': "-"
    }

    for result in Student.objects.raw(query['info'], [student_id]):
        data['s_name'] = result.s_name + " " + result.s_surname
        data['tel_no'] = result.s_tel_no
        data['email'] = result.s_email
        data['address'] = result.s_address
        data['department'] = result.d_name
        data['faculty'] = result.f_name
        data['gpax'] = result.s_gpax
        data['year'] = Current.year - result.since

    for result in Student.objects.raw(query['acivity'], [student_id]):
        data['activity'].append(result.a_name)

    for result in Student.objects.raw(query['scholarship'], [student_id]):
        data['activity'] = result.sch_name

    for result in Student.objects.raw(query['senior_project'], [student_id]):
        data['project_name'] = result.topic_name
        data['project_field'] = result.related_field
        data['project_type'] = "Senior Project"
        data['project_advisor'] = result.p_name

    for result in Student.objects.raw(query['thesis'], [student_id]):
        data['project_name'] = result.topic_name
        data['project_field'] = result.related_field
        data['project_type'] = "Thesis"
        data['project_advisor'] = result.p_name

    for result in Student.objects.raw(query['intern'], [student_id]):
        data['comp_name'] = result.comp_name

    for result in Student.objects.raw(query['exchange'], [student_id]):
        data['exchange'] = result.university_name + " in " + result.country_name

    for result in Student.objects.raw(query['status'], [student_id, Current.term]):
        data['student_status'] = result.student_status
        data['drop_status'] = result.drop_status

    for result in Student.objects.raw(query['enroll'], [student_id]):
        data['enroll'].append([result.c_name, result.grade, result.section_no_id])

    return JsonResponse(data)

def teacher(request) :
    return render(request, 'teacher.html')
def head(request) :
    return render(request, 'head.html')
def officer(request) :
    return render(request, 'officer.html')

