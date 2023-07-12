from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'polls'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('take_poll/<int:poll_id>', view=views.take_poll, name='take_poll'),
    path('completed_polls/', views.completed_polls, name='completed_polls'),
    path('completed_polls/<int:poll_id>/', views.completed_poll_detail, name='completed_poll_detail')
]