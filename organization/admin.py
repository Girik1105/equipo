from django.contrib import admin

from .models import organization, Member
# Register your models here.

admin.site.register(organization)
admin.site.register(Member)