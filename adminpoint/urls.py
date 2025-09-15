"""
URL configuration for Taskmaster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
app_name = 'adminpoint'


urlpatterns = [
    path('createtask/', views.TaskCreationView.as_view(), name='createtask'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('tasklist/', views.TaskListView.as_view(), name='tasklist'),
    path('updatetask/<int:task_id>/', views.UpdateTaskView.as_view(), name='updatetask'),
    path('deletetask/<int:task_id>/', views.DeleteTaskView.as_view(), name='deletetask'),
    path('userlist/<int:user_id>/', views.UserTaskListView.as_view(), name='userlist'),
    path('delettask/<int:task_id>/', views.delettask.as_view(), name='delettask'),
    path('completed/<int:task_id>/', views.CompletdTaskView.as_view(), name='completed'),
]
