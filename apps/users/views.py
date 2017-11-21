# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect

from django.contrib.messages import error

from .models import User

def index(request):
    print "displaying index"
    context = {
        'users' : User.objects.all()
    }
    return render(request, "users/index.html", context)

def new(request):
    print "rendering new"
    return render(request, "users/new.html")

def create(request):
    print "creating user"
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/new')
    User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        email = request.POST['email'],
    )
    user = User.objects.last()
    uid = user.id
    
    return redirect(show, uid)

def show(request, id):
    user = User.objects.get(id = id)
    return render(request, "users/show.html", {"user" : user})

def edit(request, id):
    print "editing user"
    user = User.objects.get(id = id)
    return render(request, "users/edit.html",{"user" : user})

def update(request, id):
    print "updating user"
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        print errors
        for field, message in errors.iteritems():
            error(request, message, extra_tags=field)
        return redirect('/{}/edit'.format(id))

    user = User.objects.get(id=id)
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.email = request.POST['email']
    user.save()
    uid = user.id
    return redirect(show, uid)

def destroy(request, id):
    user = User.objects.get(id = id)
    user.delete()
    return redirect('/')

