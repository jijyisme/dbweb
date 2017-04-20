from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.index, name = 'login'),
    url(r'^validate$', views.validate, name = 'validate'),
    # url(r'/teacher', views.login, name = 'teacher'),
    # url(r'/head', views.login, name = ''),
    # url(r'/officer', views.login, name = 'login'),
]
