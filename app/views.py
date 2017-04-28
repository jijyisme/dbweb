from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import json
import ast

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

    # assign static value
    Person.id = id
    Person.type = type

    return JsonResponse(data)

def query(request):

    lists = request.POST.items()
    # filter = json.dumps(lists)
    # print(lists)
    for i in lists:
        # print(i, type(i))
        # print(i[0], type(i[0]))
        dict = ast.literal_eval(i[0])
        # print(dict, type(dict))

    print(dict['tab'], dict['filter'])
    filters = dict['filter']
    selected_columns = []
    for filter in filters:
        selected_columns.append(filter[0])
    tab = dict['tab']

    print(selected_columns)

    # print(filter)
    # [["id", "none", "none"]]
    # tab = request.GET.get('tab', None)
    # print(filter)
    # print(tab)

    query = {
        'officer' : {
            'tab_student' :
                '''
                SELECT * FROM app_student S;
                ''',
        },
        'teacher' : {
            'ประวัติลงทะเบียนเรียน' :
                '''
                SELECT * FROM app_enrollment Enroll, app_student S, app_course C
                WHERE S.s_id = Enroll.s_id AND C.c_id = Enroll.c_id
                AND S.s_id IN (SELECT S.s_id FROM app_student S, app_professor P, app_supervise Supervise
                WHERE S.s_id = Supervise.s_id AND P.p_id = Supervise.p_id AND P.p_id = %s);
                ''',
            'ข้อมูลส่วนตัวนิสิต' :
                '''
                SELECT * FROM app_student S, app_professor P, app_supervise Supervise
                WHERE S.s_id = Supervise.s_id AND P.p_id = Supervise.p_id AND P.p_id = %s
                ''',
        },
        'head' : {
            'เกรดเฉลี่ยนิสิตตามชั้นปี':
                '''
                SELECT * FROM app_student S
                WHERE LEFT(S.s_id,2) = %s
                '''
        }
    }
    # if (Person.type == 'officer'):
    #     all_results = Student.objects.raw(query['officer][tab])
    # elif (Person.type == 'teacher'):
    #     all_results = Student.objects.raw(query['teacher'][tab], [id])
    # else :
    #     all_results = Student.objects.raw(query['head'][tab], ['57'])

    all_results = Student.objects.raw(query['officer'][tab])
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
            # elif column == 'c_name':
            #     data[column].append(result.c_name)
            # elif column == 'grade':
            #     data[column].append(result.grade)
            elif column == 's_name':
                data[column].append(result.s_name)
            elif column == 's_surname':
                data[column].append(result.s_surname)
    print(data)
    return JsonResponse(data)

# def render_info(request):


def student_info(request):
    s_id = request.POST.get('id', None)
    query = {
        'info' : '''
            SELECT * FROM app_student S
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
        'research' : '''
            SELECT * FROM app_student S
            JOIN app_research_owner ON app_research_owner.s_id = S.s_id
            JOIN app_research ON app_research_owner.research_id = app_research.research_id
            WHERE S.s_id = %s;
        ''',
        'status': '''
                SELECT * FROM app_student S
                JOIN app_status ON app_status.s_id = S.s_id
                WHERE S.s_id = %s AND app_status.term_year_id = %s;
            '''
    }

    student_id = s_id
    # student_id = "5730000621"
    current_term_year_id = 8

    data = {
        'id' : student_id,
        'name' : "",
        'tel_no' : "",
        'email' : "",
        'address' : "",
        'student_status' : "",
        'drop_status' : "",
        'activity' : [],
        'intern' : "-",
        'exchange' : "-",
        'research' : [],
        'enroll' : []
    }

    for result in Student.objects.raw(query['info'], [student_id]):
        data['name'] = result.s_name + " " + result.s_surname
        data['tel_no'] = result.s_tel_no
        data['email'] = result.s_email
        data['address'] = result.s_address

    for result in Student.objects.raw(query['acivity'], [student_id]):
        data['activity'].append(result.a_name)

    for result in Student.objects.raw(query['research'], [student_id]):
        data['research'].append([result.topic_name, result.type])

    for result in Student.objects.raw(query['intern'], [student_id]):
        data['internship'] = result.comp_name

    for result in Student.objects.raw(query['exchange'], [student_id]):
        data['exchange'] = [result.university_name, result.country_name, result.term_year]

    for result in Student.objects.raw(query['status'], [student_id, current_term_year_id]):
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

