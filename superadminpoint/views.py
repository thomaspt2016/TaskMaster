from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.views import View
from .forms import CustomUserCreationForm, AdminUserCreationForm
from .models import CustomUser
from apipoint.models import TaskModel
import datetime as dt
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator


def Client_required(function):
    def wrap(request, *args, **kwargs):

        if request.user.is_authenticated and request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return redirect(reverse('commn:login'))
    return wrap


@method_decorator(Client_required, name='dispatch')
class UserCreationView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'superadmin/usercreation.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usr = form.save(commit=False)
            usr.username = usr.email
            usr.save()
            return redirect('superadminpoint:usercreation')
        return render(request, 'superadmin/usercreation.html', {'form': form})


@method_decorator(Client_required, name='dispatch')
class ViewAllUsers(View):
    def get(self, request):
        users = CustomUser.objects.filter(
            Q(role='user')).select_related('assigned_admin')
        return render(request, 'superadmin/allusers.html', {'users': users})


@method_decorator(Client_required, name='dispatch')
class ViewAllAdmin(View):
    def get(self, request):
        users = CustomUser.objects.filter(role='admin')
        return render(request, 'superadmin/allusers.html', {'users': users})


@method_decorator(Client_required, name='dispatch')
class DeleteUser(View):
    def get(self, request, i):
        user = CustomUser.objects.get(id=i)
        user.delete()
        return redirect('superadminpoint:allusers')


@method_decorator(Client_required, name='dispatch')
class PromoteUser(View):
    def get(self, request, i):
        user = CustomUser.objects.get(id=i)
        user.role = 'admin'
        user.save()
        return redirect('superadminpoint:allusers')


@method_decorator(Client_required, name='dispatch')
class DemoteUser(View):
    def get(self, request, i):
        user = CustomUser.objects.get(id=i)
        user.role = 'user'
        user.assigned_admin = None
        user.save()
        return redirect('superadminpoint:allusers')


@method_decorator(Client_required, name='dispatch')
class UpdateUser(View):
    def get(self, request, i):
        user = CustomUser.objects.get(id=i)
        form = CustomUserCreationForm(instance=user)
        return render(request, 'superadmin/useredit.html', {'form': form})

    def post(self, request, i):
        user = CustomUser.objects.get(id=i)
        form = CustomUserCreationForm(request.POST, instance=user)
        print(request.POST)
        if form.is_valid():
            usr = form.save(commit=False)
            usr.username = usr.email
            usr.save()
            return redirect('superadminpoint:allusers')
        return render(request, 'superadmin/useredit.html', {'form': form})


@method_decorator(Client_required, name='dispatch')
class UpdateAdmin(View):
    def get(self, request, i):
        user = CustomUser.objects.get(id=i)
        form = AdminUserCreationForm(instance=user)
        return render(request, 'superadmin/useredit.html', {'form': form})

    def post(self, request, i):
        user = CustomUser.objects.get(id=i)
        form = AdminUserCreationForm(request.POST, instance=user)
        print(request.POST)
        if form.is_valid():
            usr = form.save(commit=False)
            usr.username = usr.email
            usr.save()
            return redirect('superadminpoint:allusers')
        return render(request, 'superadmin/useredit.html', {'form': form})


@method_decorator(Client_required, name='dispatch')
class taskListView(View):
    def get(self, request):
        tasks = TaskModel.objects.all()
        return render(request, 'superadmin/tasklist.html', {'tasks': tasks})


@method_decorator(Client_required, name='dispatch')
class CompletdTaskView(View):
    def get(self, request, task_id):
        task = TaskModel.objects.get(id=task_id)
        return render(request, 'superadmin/completed.html', {'task': task})


@method_decorator(Client_required, name='dispatch')
class UpdateTaskView(View):
    def get(self, request, task_id):
        task = TaskModel.objects.get(id=task_id)
        users = CustomUser.objects.filter(Q(role='user') | Q(role='admin'))
        today = dt.date.today().isoformat()
        return render(request, 'superadmin/updatetask.html', {'task': task, 'users': users, 'today': today})

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


@method_decorator(Client_required, name='dispatch')
class DeleteTaskView(View):
    def get(self, request, task_id):
        task = TaskModel.objects.get(id=task_id)
        task.delete()
        return redirect('superadminpoint:tasklist')


@method_decorator(Client_required, name='dispatch')
class UserTasksView(View):
    def get(self, request, user_id):
        print("inside")
        user = CustomUser.objects.get(id=user_id)
        tasks = TaskModel.objects.filter(assignedto=user)
        return render(request, 'superadmin/tasklist.html', {'tasks': tasks})


@method_decorator(Client_required, name='dispatch')
class AdminTaskView(View):
    def get(self, request, user_id):
        print(user_id)
        tasks = TaskModel.objects.filter(supervisor=user_id)
        return render(request, 'superadmin/tasklist.html', {'tasks': tasks})