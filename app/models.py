from django.db import models

# Create your models here.
# class Person(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#
#     def __str__(self):
#         return "Mr." + self.first_name + " " + self.last_name


#-------------- ENTITY --------------

class Faculty(models.Model):
    f_id = models.CharField(max_length=10, primary_key=True, default="0000000000")
    f_name = models.CharField(max_length=45)

class Department(models.Model):
    d_id = models.CharField(max_length=10, primary_key=True, default="0000000000")
    d_name = models.CharField(max_length=60)
    f = models.ForeignKey(Faculty, on_delete=models.CASCADE)

class Student(models.Model):
    d = models.ForeignKey(Department)
    s_id = models.CharField(max_length=10, primary_key=True, default="0000000000")
    s_name = models.CharField(max_length=30)
    s_surname = models.CharField(max_length=50)
    s_tel_no = models.CharField(max_length=10)
    s_email = models.CharField(max_length=30)
    s_address = models.CharField(max_length=100)
    s_password = models.CharField(max_length=16)

class Activity(models.Model):
    a_id = models.CharField(max_length=10, primary_key=True, default="0000000000")
    a_name = models.CharField(max_length=45)

class Award(models.Model):
    award_id = models.CharField(max_length=10, primary_key=True, default="0000000000")
    award_name = models.CharField(max_length=45)
    description = models.CharField(max_length=100)

class Company(models.Model):
    comp_id = models.CharField(max_length=20, primary_key=True, default="00000000000000000000")
    comp_name = models.CharField(max_length=60)
    comp_tel_no = models.CharField(max_length=10)
    comp_address = models.CharField(max_length=100)

class Course(models.Model):
    c_id = models.CharField(max_length=7, primary_key=True, default="0000000")
    c_name = models.CharField(max_length=30)
    credit = models.DecimalField

class Exchange_program(models.Model):
    ex_id = models.CharField(max_length=10, primary_key=True, default="0000000000")
    university_name = models.CharField(max_length=45)
    country_name = models.CharField(max_length=45)

class Professor(models.Model):
    d = models.ForeignKey(Department, on_delete=models.CASCADE)
    p_id = models.CharField(max_length=10, primary_key=True, default="0000000000")
    p_name = models.CharField(max_length=30)
    p_surname = models.CharField(max_length=50)
    p_tel_no = models.CharField(max_length=10)
    p_email = models.CharField(max_length=30)
    p_address = models.CharField(max_length=100)
    p_password = models.CharField(max_length=16)
    p_picture = models.FileField()

class Officer(models.Model):
    d = models.ForeignKey(Department, on_delete=models.CASCADE)
    o_id = models.CharField(max_length=10, primary_key=True, default="0000000000")
    o_name = models.CharField(max_length=30)
    o_surname = models.CharField(max_length=50)
    o_password = models.CharField(max_length=16)
    o_picture = models.FileField()

class Research(models.Model):
    p = models.ForeignKey(Professor)
    research_id = models.CharField(max_length=20, primary_key=True, default="00000000000000000000")
    topic_name = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    related_field = models.CharField(max_length=100)

class Scholarship(models.Model):
    sch_id = models.CharField(max_length=10, primary_key=True, default="0000000000")
    sch_name = models.CharField(max_length=45)
    type = models.CharField(max_length=10)
    amount = models.IntegerField

class Section(models.Model):
    c = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_no = models.CharField(max_length=2, primary_key=True, default="0")
    time = models.CharField(max_length=20)
    day = models.CharField(max_length=10)
    classroom = models.CharField(max_length=4)
    building = models.CharField(max_length=10)
    class Meta:
        unique_together = (('c', 'section_no'),)

class Semester(models.Model):
    term_year = models.CharField(max_length=6)

class Tuition_fee(models.Model):
    d = models.ForeignKey(Department, on_delete=models.CASCADE)
    fee = models.IntegerField(primary_key=True, default=0)
    class Meta:
        unique_together = (('fee', 'd'),)

class Graduated(models.Model):
    s = models.ForeignKey(Student, on_delete=models.CASCADE)

class Undergraduated(models.Model):
    s = models.ForeignKey(Student, on_delete=models.CASCADE)


#-------------- RELATIONAL --------------

class Activity_participation(models.Model):
    a = models.ForeignKey(Activity)
    s = models.ForeignKey(Student)
    since = models.DateField

class Enrollment(models.Model):
    grade = models.CharField(max_length=1)
    c = models.ForeignKey(Course)
    s = models.ForeignKey(Student)
    term_year = models.ForeignKey(Semester)
    section_no = models.ForeignKey(Section)

class Get_award(models.Model):
    s = models.ForeignKey(Student)
    award = models.ForeignKey(Award)
    term_year = models.ForeignKey(Semester)

class Get_scholarship(models.Model):
    s = models.ForeignKey(Student)
    sch = models.ForeignKey(Scholarship)
    term_year = models.ForeignKey(Semester)

class Manage_dept(models.Model):
    p = models.ForeignKey(Professor)
    d = models.ForeignKey(Department)
    since = models.DateField

class Manage_faculty(models.Model):
    p = models.ForeignKey(Professor)
    f = models.ForeignKey(Faculty)
    since = models.DateField

class Interns(models.Model):
    s = models.ForeignKey(Student)
    comp = models.ForeignKey(Company)
    intern_advisor = models.CharField(max_length=80)

class Payment(models.Model):
    s = models.ForeignKey(Student)
    d = models.ForeignKey(Department)
    fee = models.ForeignKey(Tuition_fee)
    term_year = models.ForeignKey(Semester)


class Research_owner(models.Model):
    research = models.ForeignKey(Research)
    s = models.ForeignKey(Student)

class Status(models.Model):
    s = models.ForeignKey(Student)
    term_year = models.ForeignKey(Semester)
    student_status = models.CharField(max_length=10)
    drop_status = models.CharField(max_length=10)

class Supervise(models.Model):
    s = models.ForeignKey(Student)
    p = models.ForeignKey(Professor)
    since = models.DateField

class TA(models.Model):
    s = models.ForeignKey(Student)
    c = models.ForeignKey(Course)
    section_no = models.ForeignKey(Section)
    term_year = models.ForeignKey(Semester)

class Take_exchange_program(models.Model):
    s = models.ForeignKey(Student)
    ex = models.ForeignKey(Exchange_program)
    term_year = models.ForeignKey(Semester)

class Teach(models.Model):
    p = models.ForeignKey(Professor)
    c = models.ForeignKey(Course)
    section_no = models.ForeignKey(Section)
    term_year = models.ForeignKey(Semester)
