from django.urls import path
from . import views

app_name = 'birthdays'

urlpatterns = [
    path('', views.index, name='index'),
]
