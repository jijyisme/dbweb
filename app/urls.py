from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.index, name = 'login'),
    url(r'^validate$', views.validate, name = 'validate'),
    url(r'^query$', views.query, name = 'query'),
    url(r'teacher', views.teacher, name = 'Profile'),
    url(r'head', views.head, name = 'Profile'),
    url(r'officer', views.officer, name = 'Profile'),
]
