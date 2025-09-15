from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.views import View
from .forms import LoginForm
from django.http import HttpResponse
# Create your views here.


class SignInView(View):
    def get(self,request):
        form = LoginForm()
        return render(request, 'loginform.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('superadminpoint:usercreation')
                elif user.role == 'admin':
                    return redirect('adminpoint:createtask')
            else:
                form.add_error(None, 'Invalid username or password')
        return render(request, 'loginform.html', {'form': form})

class SignOutView(View):
    def get(self,request):
        logout(request)
        return redirect('commn:login')