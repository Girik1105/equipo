from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

from ckeditor.fields import RichTextField
from django.urls import reverse

import uuid

# Create your models here.
class doodle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    body = RichTextField(blank=True, null=True)

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        ordering = ['-timestamp']


class to_do(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    is_complete = models.BooleanField(default=False)

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        ordering = ['is_complete', 'due_date']