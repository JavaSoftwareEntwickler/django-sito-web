from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm, CreateUserForm, LoginForm
from . constants import ImageWidth
from PIL import Image
from .utils import get_new_image_dimensions, resize_image
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import formats
import os

def homepage(request):
    return render(request,'crm/index.html')

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registrato con successo!")
            return redirect('my-login/')
    
    context = {'FormUser':form}
    return render(request, 'crm/register.html', context)

def my_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard/')
    form = LoginForm()
    context = { 'LoginForm': form }
    return render(request, 'crm/my-login.html', context)

@login_required(login_url='my-login/')
def dashboard(request):
    return render(request, 'crm/dashboard.html')

def user_logout(request):
    auth.logout(request)
    return render(request, 'crm/index.html')

def info(request):
    return render(request, 'crm/info.html')

@login_required(login_url='my-login/')
def taskById(request):
    data = Task.objects.get(id=7)
    context = {'task': data}
    return render(request, 'crm/task.html', context)


'''
GET ALL BY ID USER 
'''
@login_required(login_url='my-login/')
def tasks(request):
    data = Task.objects.all().filter(user=request.user.id)
    for i in range(len(data)):
        data[i].data_ins = formats.date_format(data[i].data_ins, "SHORT_DATETIME_FORMAT")
    context = {'tasks': data}
    return render(request, 'crm/view-tasks.html', context)


'''
ADD NEW 
'''
@login_required(login_url='my-login/')
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task = form.save()
            return redirect('view-tasks/')
    form = TaskForm
    context = {'form':form}
    return render(request, 'crm/create-task.html', context)


'''
UPDATE 
'''
@login_required(login_url='my-login/')
def update_task(request, pk):
    try:
        task = Task.objects.get(id=pk, user=request.user)
    except:
        return redirect('view-tasks/')
    
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid:
            #if task.img.name != form.fields['img']:
            if 'img' in request.FILES:
                if task.img:
                    task.img.delete()
            form.save()
            return redirect('view-tasks/')
    context = {'updateTask': form}
    return render(request, 'crm/update-task.html', context)


'''
DELETE
'''
@login_required(login_url='my-login/')
def delete_task(request, pk):
    try:
        task = Task.objects.get(id=pk, user=request.user)
    except:
        return redirect('view-tasks/')
    if request.method == 'POST':
        if task.img:
            task.img.delete()
        task.delete()
        return redirect('view-tasks/')
    return render(request, 'crm/delete-task.html')


