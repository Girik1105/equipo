from django.urls import path

from . import views

urlpatterns = [
    path('edit/', views.profile_edit_view, name="edit-user-profile"),
]
