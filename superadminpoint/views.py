from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.views import View
from .forms import CustomUserCreationForm,AdminUserCreationForm
from .models import CustomUser
from apipoint.models import TaskModel
import datetime as dt

# Create your views here.

class UserCreationView(View):
    def get(self,request):
        form = CustomUserCreationForm()
        return render(request,'superadmin/usercreation.html',{'form':form})
    
    def post(self,request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usr = form.save(commit=False)
            usr.username = usr.email
            usr.save()
            return redirect('superadminpoint:usercreation')
        return render(request,'superadmin/usercreation.html',{'form':form})

class ViewAllUsers(View):
    def get(self,request):
        users = CustomUser.objects.filter(Q(role='user')).select_related('assigned_admin')
        return render(request,'superadmin/allusers.html',{'users':users})

class ViewAllAdmin(View):
    def get(self,request):
        users = CustomUser.objects.filter(role='admin')
        return render(request,'superadmin/allusers.html',{'users':users})

class DeleteUser(View):
    def get(self,request,i):
        user = CustomUser.objects.get(id=i)
        user.delete()
        return redirect('superadminpoint:allusers')

class PromoteUser(View):
    def get(self,request,i):
        user = CustomUser.objects.get(id=i)
        user.role = 'admin'
        user.save()
        return redirect('superadminpoint:allusers')

class DemoteUser(View):
    def get(self,request,i):
        user = CustomUser.objects.get(id=i)
        user.role = 'user'
        user.assigned_admin = None
        user.save()
        return redirect('superadminpoint:allusers')

class UpdateUser(View):
    def get(self, request, i):
        user = CustomUser.objects.get(id=i)
        form = CustomUserCreationForm(instance=user)
        return render(request, 'superadmin/useredit.html', {'form':form})
    def post(self, request, i):
        user = CustomUser.objects.get(id=i)
        form = CustomUserCreationForm(request.POST, instance=user)
        print(request.POST)
        if form.is_valid():
            usr = form.save(commit=False)
            usr.username = usr.email
            usr.save()
            return redirect('superadminpoint:allusers')
        return render(request, 'superadmin/useredit.html', {'form':form})

class UpdateAdmin(View):
    def get(self, request, i):
        user = CustomUser.objects.get(id=i)
        form = AdminUserCreationForm(instance=user)
        return render(request, 'superadmin/useredit.html', {'form':form})
    def post(self, request, i):
        user = CustomUser.objects.get(id=i)
        form = AdminUserCreationForm(request.POST, instance=user)
        print(request.POST)
        if form.is_valid():
            usr = form.save(commit=False)
            usr.username = usr.email
            usr.save()
            return redirect('superadminpoint:allusers')
        return render(request, 'superadmin/useredit.html', {'form':form})
    
class taskListView(View):
    def get(self, request):
        tasks = TaskModel.objects.all()
        return render(request, 'admin/tasklist.html', {'tasks':tasks})
    
class CompletdTaskView(View):
    def get(self, request, task_id):
        task = TaskModel.objects.get(id=task_id)
        return render(request, 'superadmin/completed.html', {'task':task})

    
class UpdateTaskView(View):
    def get(self, request, task_id):
        task = TaskModel.objects.get(id=task_id)
        users = CustomUser.objects.filter(Q(role='user') | Q(role='admin') )
        today = dt.date.today().isoformat()
        return render(request, 'admin/updatetask.html', {'task':task, 'users':users, 'today':today})
    def post(self, request, task_id):
        task = TaskModel.objects.get(id=task_id)
        title = request.POST.get('title')
        description = request.POST.get('description')
        assignedto = request.POST.get('assignedto')
        duedate = request.POST.get('duedate')
        if duedate:
            duedate = dt.datetime.strptime(duedate, '%Y-%m-%d').date()

        if title and description and assignedto and duedate:
            task.title = title
            task.description = description
            task.assignedto = CustomUser.objects.get(id=assignedto)
            task.duedate = duedate
            task.save()
            return redirect('superadminpoint:tasklist')

class DeleteTaskView(View):
    def get(self, request, task_id):
        task = TaskModel.objects.get(id=task_id)
        task.delete()
        return redirect('superadminpoint:tasklist')
class UserTasksView(View):
    def get(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        tasks = TaskModel.objects.filter(assignedto=user)
        return render(request, 'admin/tasklist.html', {'tasks':tasks})