from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse

from django.contrib.auth.decorators import login_required
from django.http import Http404

from django.contrib.auth import get_user_model
User = get_user_model()

from django.db.models import Q

from . import forms, models
from accounts import models as account_models

from django.core.mail import send_mail
from django.utils import timezone 

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
    members = models.Member.objects.filter(organization=org, is_verified=True)

    kwargs = {}
    kwargs.update({"org": org})
    # kwargs.update({"members": members})
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
        "item":org,
    }

    return render(request, 'organization/edit_org.html', context)


@login_required
def detail_organization(request, slug): 

    org = get_object_or_404(models.organization, slug=slug)
    work = models.work.objects.filter(organization=org)
    members = models.Member.objects.filter(organization=org, is_verified=True)
    unverified_members = models.Member.objects.filter(organization=org, is_verified=False)

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
                    form.instance.is_verified = False
                    form.save(commit=True)

                    send_mail(
                        subject=f"You were added to { org.name }",
                        message=f"You have been add as a member in { org.name }. please go to your dashboard to verify your membership. \n Organisation details: \n Name: { org.name } \n Description: { org.description } \n Members: { org.members.all().count() }",
                        from_email='test@test.com',
                        recipient_list=[form.instance.user.email]
                    )

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
        "all_work":work,
        "members":members,
        "unverified_members":unverified_members,
    }

    return  render(request, 'organization/org_detail.html', context)

@login_required
def create_work(request, slug):
    org = models.organization.objects.get(slug=slug)
    members = models.Member.objects.filter(organization=org, is_verified=True)

    if not request.user == org.owner or request.user in org.admins.all():
        raise Http404

    kwargs = {}
    kwargs.update({"org": org})
    # kwargs.update({"members": members})
    form = forms.create_work_form(**kwargs)

    if request.method == "POST":
        if request.user == org.owner or request.user in org.admins.all():
            form = forms.create_work_form(request.POST, **kwargs)
            if form.is_valid():
                form.save(commit=False)
                form.instance.organization = org
                form.instance.creator = request.user
                form.save()
                send_mail(
                    subject=f"Work assigned in { org.name }",
                    message=f"You have been assigned with some work. Go to { org.name }'s page to view it. \n Work Details: \n Title: { form.instance.title } \n Description: { form.instance.description } \n Due: { form.instance.due_date }",
                    from_email='test@test.com',
                    recipient_list=[form.instance.assigned_to.email]
                )
                return redirect(reverse('org:detail-org', kwargs={"slug":org.slug}))
            else:
                return redirect(reverse('org:detail-org', kwargs={"slug":org.slug}))
        else:
            raise Http404
    else:
        form = forms.create_work_form(**kwargs)
    
    context = {
        "form":form,
        "item":org,
    }

    return render(request, 'organization/work/create_work.html', context)

@login_required
def edit_work(request, slug, pk):
    org = models.organization.objects.get(slug=slug)

    work = models.work.objects.get(organization=org, pk=pk)

    if not request.user == org.owner or request.user not in org.admins.all():
        raise Http404

    kwargs = {}
    kwargs.update({"org": org})
    form = forms.create_work_form(instance=work, **kwargs)

    if request.method == "POST":
        if request.user == org.owner or request.user in org.admins.all():
            form = forms.create_work_form(request.POST, instance=work, **kwargs)
            if form.is_valid():
                form.save(commit=False)
                form.instance.organization = org
                form.instance.creator = request.user
                form.save()
                return redirect(reverse('org:detail-org', kwargs={"slug":org.slug}))
            else:
                return redirect(reverse('org:detail-org', kwargs={"slug":org.slug}))
        else:
            raise Http404
    else:
        form = forms.create_work_form(instance=work, **kwargs)
    
    context = {
        "form":form,
        "item":org,
    }

    return render(request, 'organization/work/edit_work.html', context)

@login_required
def update_work(request, pk, slug):
    org = models.organization.objects.get(slug=slug)

    try:
        work = models.work.objects.get(assigned_to=request.user, pk=pk)
    except:
        raise Http404


    form = forms.update_work_form(instance=work)

    if request.method == "POST":
            form = forms.update_work_form(request.POST, request.FILES, instance=work)
            if form.is_valid():
                form.save(commit=False)
                form.instance.organization = org
                send_mail(
                    subject=f"Work assigned by you is completed",
                    message=f"The work you assigned by you to { request.user.profile.name } is completed . Go to { org.name }'s page to view it. \n Work Details: \n Title: { form.instance.title } \n Description: { form.instance.description } \n Date completed: { timezone.now().date() }",
                    from_email='test@test.com',
                    recipient_list=[form.instance.creator.email]
                )
                form.save()
                return redirect(reverse('org:detail-org', kwargs={"slug":org.slug}))
            else:
                return redirect(reverse('org:detail-org', kwargs={"slug":org.slug}))
    else:
        form = forms.update_work_form(instance=work)
    
    context = {
        "form":form,
        "item":org,
    }

    return render(request, 'organization/work/update_work.html', context)

@login_required
def detail_work(request, pk, slug):
    org = models.organization.objects.get(slug=slug)

    try:
        work = models.work.objects.get(pk=pk)
    except:
        raise Http404
    
    context = {
        "item":org,
        "work": work,
    }

    return render(request, 'organization/work/detail_work.html', context)

@login_required
def leave_organization(request, slug):
    org = models.organization.objects.get(slug=slug)
    member = models.Member.objects.get(user=request.user, organization=org)
    
    if org.owner == request.user:
        oldest_member = models.Member.objects.filter(organization=org).order_by('joined_since')[1:2].first()
        org.owner = oldest_member.user
        org.save()
    
    member.delete()

    return redirect('dashboard:list-organizations')

def verify_membership(request, slug):
    org = models.organization.objects.get(slug=slug)
    member = models.Member.objects.get(user=request.user, organization=org)
    member.is_verified = True
    member.save()

    return redirect(reverse('org:detail-org', kwargs={"slug":org.slug}))