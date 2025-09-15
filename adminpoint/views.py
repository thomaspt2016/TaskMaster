from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.views import View
from superadminpoint.models import CustomUser
from apipoint.models import TaskModel
import datetime as dt


class TaskCreationView(View):
    def get(self,request):
        users = CustomUser.objects.filter(Q(role='user') & Q(assigned_admin=request.user.id))
        today = dt.date.today().isoformat()
        return render(request, 'admin/CreateTask.html', {'users': users, 'today': today})
    
    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        assignedto = request.POST.get('assignedto')
        duedate = request.POST.get('duedate')
        if duedate:
            duedate = dt.datetime.strptime(duedate, '%Y-%m-%d').date()
        if title and description and assignedto and duedate:
            task = TaskModel(title=title, description=description, 
                             assignedto=CustomUser.objects.get(id=assignedto), 
                             duedate=duedate, supervisor=CustomUser.objects.get(id=request.user.id))
            task.save()
            return redirect('adminpoint:createtask')
    
class UsersView(View):
    def get(self,request):
        users = CustomUser.objects.filter(assigned_admin=request.user.id)
        return render(request,'superadmin/allusers.html',{'users':users})

class TaskListView(View):
    def get(self, request):
        tasks = TaskModel.objects.filter(supervisor=request.user.id)
        return render(request, 'admin/tasklist.html', {'tasks':tasks})
    
class UpdateTaskView(View):
    def get(self, request, task_id):
        task = TaskModel.objects.get(id=task_id)
        users = CustomUser.objects.filter(Q(role='user') & Q(assigned_admin=request.user.id))
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
            return redirect('adminpoint:tasklist')

class DeleteTaskView(View):
    def get(self, request, task_id):
        task = TaskModel.objects.get(id=task_id)
        task.delete()
        return redirect('adminpoint:tasklist')
    
class UserTaskListView(View):
    def get(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        tasks = TaskModel.objects.filter(assignedto=user)
        return render(request, 'admin/tasklist.html', {'tasks':tasks})

class delettask(View):
    def get(self, request, task_id):
        task = TaskModel.objects.get(id=task_id)
        task.delete()
        return redirect('adminpoint:tasklist')
    
