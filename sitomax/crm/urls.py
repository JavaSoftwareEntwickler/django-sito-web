from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name=""),
    path('register/', views.register, name="register/"),
    path('my-login/', views.my_login, name="my-login/"),
    path('info/', views.info, name="info/"),
    path('dashboard/', views.dashboard, name="dashboard/"),
    path('user-logout/', views.user_logout, name="/"),
    path('task/', views.taskById, name="task/"),
    path('view-tasks/', views.tasks, name="view-tasks/"),
    path('create-task/', views.create_task, name="create-task/"),
    path('update-task/<str:pk>', views.update_task, name="update-task"),
    path('delete-task/<str:pk>', views.delete_task, name="delete-task"),
]




