from django.urls import path

from . import views

app_name = 'org'

urlpatterns = [
    path('create/', views.create_organization, name='create-org'),
    path('<slug>/', views.detail_organization, name='detail-org'),
    path('update/<slug>/', views.update_organization, name='update-org'),

]
