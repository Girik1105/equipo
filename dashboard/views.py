from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from django.http import Http404

from django.utils import timezone

from . import models, forms
from organization.models import Member, organization

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

# Homepage
@login_required
def index(request):
    doodles = models.doodle.objects.filter(user=request.user)
    todos = models.to_do.objects.filter(user=request.user)
    today = timezone.now().date()
    todo_today = models.to_do.objects.filter(user=request.user, is_complete=False, due_date=today)
    context = {
        "todo":todos,
        "doodles":doodles,
        "todo_today":todo_today,
    }
    return render(request, 'dashboard/index.html', context)

# DOODLES CRUD
@login_required
def create_doodle(request):
    doodle_form = forms.doodle_form()
    if request.method == 'POST':
        form = forms.doodle_form(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.user = request.user
            form.save(commit=True)
            return redirect('dashboard:doodles')
        else:
            form = forms.doodle_form()

    context = {
        "form":doodle_form
    }
    return render(request, 'dashboard/doodles/doodle_create.html', context)


@login_required
def list_doodle(request):
    all_doodles = models.doodle.objects.filter(user=request.user)
    context = {
        "all_doodles": all_doodles,
    }
    return render(request, 'dashboard/doodles/doodle_list.html', context)


@login_required
def detail_doodle(request, pk):
    try:
        doodle = models.doodle.objects.get(user=request.user, pk=pk)
    except:
        raise Http404

    context = {
        'doodle':doodle
    }
    return render(request, 'dashboard/doodles/doodle_detail.html', context)


def download_doodle(request, pk):
    try:
        obj = models.doodle.objects.get(user=request.user, pk=pk)
    except:
        raise Http404
        
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 100, obj.title)
    p.drawString(150, 150, obj.body)

    p.showPage()
    p.save()

    title = f"{ obj.title }.pdf"
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=title)

@login_required
def edit_doodle(request, pk):
    try:
        doodle = models.doodle.objects.get(user=request.user, pk=pk)
    except:
        raise Http404
    
    doodle_form = forms.doodle_form(instance=doodle)
    if request.method == 'POST':
        form = forms.doodle_form(request.POST, instance=doodle)
        if form.is_valid():
            form.save()
            return redirect('dashboard:doodles')
        else:
            form = forms.doodle_form(instance=doodle)

    context = {
        "form":doodle_form
    }

    return render(request, 'dashboard/doodles/doodle_edit.html', context)


@login_required
def delete_doodle(request, pk):
    try:
        doodle = models.doodle.objects.get(user=request.user, pk=pk)
    except:
        raise Http404
    
    if request.method == 'POST':
        if request.user == doodle.user:
            doodle.delete()
            return redirect('dashboard:doodles')
        else:
            return redirect('dashboard:doodles')

    context = {
        "doodle":doodle
    }

    return render(request, 'dashboard/doodles/doodle_delete.html', context)

# TODO CRUD 
@login_required
def create_todo(request):
    todo_form = forms.todo_form()
    if request.method == 'POST':
        form = forms.todo_form(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.user = request.user
            form.save(commit=True)
            return redirect('dashboard:todo')
        else:
            form = forms.todo_form()

    context = {
        "form":todo_form
    }
    return render(request, 'dashboard/todo/todo_create.html', context)

    
@login_required
def list_todo(request):
    all_todo = models.to_do.objects.filter(user=request.user)
    context = {
        "all_todo": all_todo,
    }
    return render(request, 'dashboard/todo/todo_list.html', context)

@login_required
def complete_todo(request, pk):
    try:
        todo = models.to_do.objects.get(user=request.user, pk=pk)
    except:
        raise Http404
    todo.is_complete = True
    todo.save()
    context = {}
    return redirect('dashboard:todo')

@login_required
def delete_todo(request, pk):
    try:
        todo = models.to_do.objects.get(user=request.user, pk=pk)
    except:
        raise Http404
    if request.method == 'POST':
        todo.delete()
        return redirect('dashboard:todo')
    context = {
        "todo": todo,
    }
    return render(request, 'dashboard/todo/todo_delete.html', context)

@login_required
def show_organizations(request):
    
    orgs = organization.objects.filter(members=request.user)

    context = {
        'organizations':orgs
    }

    return render(request, 'dashboard/organizations/org_list.html', context)
