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
app_name = 'superadminpoint'

urlpatterns = [
    path('usercreation/', views.UserCreationView.as_view(), name='usercreation'),
    path('allusers/', views.ViewAllUsers.as_view(), name='allusers'),
    path('adminusers/', views.ViewAllAdmin.as_view(), name='adminusers'),
    path('deleteuser/<int:i>/', views.DeleteUser.as_view(), name='deleteuser'),
    path('promoteuser/<int:i>/', views.PromoteUser.as_view(), name='promoteuser'),
    path('demoteuser/<int:i>/', views.DemoteUser.as_view(), name='demoteuser'),
    path('updateuser/<int:i>/', views.UpdateUser.as_view(), name='updateuser'),
    path('updateadmin/<int:i>/', views.UpdateAdmin.as_view(), name='updateadmin'),
    path('tasklist/', views.taskListView.as_view(), name='tasklist'),
    path('completed/<int:task_id>/', views.CompletdTaskView.as_view(), name='completed'),
    path('updatetask/<int:task_id>/', views.UpdateTaskView.as_view(), name='updatetask'),
    path('deletetask/<int:task_id>/', views.DeleteTaskView.as_view(), name='deletetask'),
]
