from django.db import models

from django.contrib.auth import get_user_model, login
from django.views.generic.edit import DeleteView
User = get_user_model()

from django.db.models.signals import post_save, pre_save
from django.shortcuts import get_object_or_404
from django.dispatch import receiver

from django.utils.text import slugify

from django.urls import reverse

# Create your models here.
class organization(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    owner = models.ForeignKey(User, blank=True, related_name='admin', on_delete= models.CASCADE)
    admins = models.ManyToManyField(User, blank=True, related_name='group_moderators')
    members = models.ManyToManyField(User, through='Member')
    cover = models.ImageField(upload_to='uploads/covers', default='uploads/covers/default.jpg', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail-group', kwargs={'slug':self.slug})

    class Meta():
        ordering = ["-created_on"]


class Member(models.Model):
    organization = models.ForeignKey(organization, related_name='membership', on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name='user_organizations', on_delete = models.CASCADE)
    joined_since = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    class Meta():
        unique_together = ('user', 'organization')

@receiver(pre_save, sender=organization)
def organization_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
    
@receiver(post_save, sender=organization)
def organization_save_member(sender, instance, created, *args, **kwargs):
    if not organization.objects.filter(user=instance.owner, organization=instance).exists():
        organization.objects.create(user=instance.owner, organization=instance)

