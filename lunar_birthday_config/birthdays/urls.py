from django.urls import path
from . import views

app_name = 'birthdays'

urlpatterns = [
    path('', views.index, name='index'),
    path('set_language/<str:language>/', views.set_language, name='set_language'),
]
