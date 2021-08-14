"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views
from accounts.views import account_signup_view

from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("accounts/signup/", view=account_signup_view, name='register'),
    path('accounts/', include('allauth.urls')),
    
    path('user/profile/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('organizations/', include('organization.urls')),

    path('', views.index, name="index"),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
]

handler404 = 'project.views.error_404'
handler403 = 'project.views.error_403'

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
