from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm, CreateUserForm, LoginForm
from . constants import ImageWidth
from PIL import Image
from .utils import get_new_image_dimensions, resize_image, invio_messaggio_mail
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import formats

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



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
                invio_messaggio_mail(user.email, 'Un nuovo dispositivo sta usando il tuo account', f"<strong>Un nuovo dispositivo sta usando il tuo account..</strong>Ciao {user.username},\nun nuovo dispositivo ha effettuato l'accesso al tuo account digitalWorld,\n{user.email}.")
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


def invio_mail(request):
    message = Mail(
        from_email=os.getenv('FROM_MAIL'),
        to_emails=os.getenv('TO_MAIL'),
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f'status code : {response.status_code}')
        print(f'response body : {response.body}')
        print(f'response headers : {response.headers}')
    except Exception as e:
        print(e.message)
        return redirect('view-tasks/')
    return render(request, 'crm/view-tasks.html')

