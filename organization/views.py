from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse

from django.contrib.auth.decorators import login_required
from django.http import Http404

from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models import Q

from . import forms, models
from accounts import models as account_models
# Create your views here.

@login_required
def create_organization(request): 

    org_form = forms.create_organization_form()

    if request.method == 'POST':
        form = forms.create_organization_form(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            form.instance.owner = request.user
            form.save(commit=True)

            return redirect(reverse('org:detail-org', kwargs={"slug":form.instance.slug}))
    else:
        org_form = forms.create_organization_form()
            
    context = {
        "org_form": org_form,
    }

    return render(request, 'organization/create_org.html', context)


@login_required
def update_organization(request, slug): 

    org = get_object_or_404(models.organization, slug=slug)

    kwargs = {}
    kwargs.update({"org": org})
    org_form = forms.update_organization_form(instance=org, **kwargs)

    if request.user == org.owner:
        if request.method == 'POST':
            form = forms.update_organization_form(request.POST, request.FILES, instance=org, **kwargs)
            if form.is_valid():
                form.save()
                return redirect(reverse('org:detail-org', kwargs={"slug":org.slug}))
        else:
            org_form = forms.update_organization_form(instance=org, **kwargs)
    else:
        return HttpResponse(status=403)
        
    context = {
        "org_form": org_form,
    }

    return render(request, 'organization/create_org.html', context)


@login_required
def detail_organization(request, slug): 

    org = get_object_or_404(models.organization, slug=slug)

    if not models.Member.objects.filter(organization=org, user=request.user, is_verified=True).exists():
        raise Http404
    
    form = forms.add_member()

    if request.method == "POST":
        if request.user == org.owner or request.user in org.admins.all():
            form = forms.add_member(request.POST)
            if form.is_valid():
                if form.instance.user not in org.members.all():
                    form.save(commit=False)
                    form.instance.organization = org
                    form.instance.is_verified = True
                    form.save(commit=True)
                    return redirect(reverse('org:detail-org', kwargs={"slug":org.slug}))
            else:
                return redirect(reverse('org:detail-org', kwargs={"slug":org.slug}))
        else:
            return redirect(reverse('org:detail-org', kwargs={"slug":org.slug}))

    else:
        form = forms.add_member()

    context = {
        "item": org,
        "member_form":form,
    }

    return  render(request, 'organization/org_detail.html', context)
