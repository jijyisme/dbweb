from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^$', views.login, name = 'login'),
    url(r'/teacher', views.login, name = 'teacher'),
    url(r'/head', views.login, name = ''),
    url(r'/officer', views.login, name = 'login'),
]
