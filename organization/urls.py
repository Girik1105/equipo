from django.urls import path

from . import views

app_name = 'org'

urlpatterns = [
    path('create/', views.create_organization, name='create-org'),
    path('update/<slug>/', views.update_organization, name='update-org'),
    path('<slug>/', views.detail_organization, name='detail-org'),

    path('verify/member/<slug>/', views.verify_membership, name='verify-member'),
    path('leave/<slug>/', views.leave_organization, name='leave-org'),

    path('work/create/<slug>/', views.create_work, name='create-work'),
    path('work/complete/<int:pk>/<slug>/', views.update_work, name='update-work'),
    path('work/edit/<int:pk>/<slug>/', views.edit_work, name='edit-work'),
    path('work/detail/<int:pk>/<slug>/', views.detail_work, name='detail-work'),
]