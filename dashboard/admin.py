from django.contrib import admin
from .models import doodle, to_do

# Register your models here.
admin.site.register(doodle)
admin.site.register(to_do)