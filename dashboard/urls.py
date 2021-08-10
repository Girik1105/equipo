from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name="index"),
    path('create-doodle/', views.create_doodle, name="create-doodle"),
    path('doodles/', views.list_doodle, name="doodles"),
    path('doodles/<str:pk>', views.detail_doodle, name="doodles-detail"),
    path('doodles/edit/<str:pk>', views.edit_doodle, name="doodles-edit"),
    path('doodles/delete/<str:pk>', views.delete_doodle, name="doodles-delete"),

    path('todo-list/', views.list_todo, name="todo"),
    path('todo-list/add/', views.create_todo, name="todo-create"),
    path('todo-list/task/<str:pk>/complete/', views.complete_todo, name="todo-complete"),
]
