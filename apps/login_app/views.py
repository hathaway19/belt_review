# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
    # User.objects.all().delete()
    all_users = User.objects.all()
    for user in all_users:
        print "___________________________________________________"
        print user.name, user.email
    return render(request, 'login_app/index.html')

# Method to create a new user
def register(request):
    # Sends user submitted data to models.py to validate the information
    # If it's valid, a new user is created
    results = User.objects.register(request.POST)

    # If valid, gives success message
    if results['valid']:
        messages.success(request, "You have successfully registered. Please log in.")
    # List all errors if it's invalid
    else:
        for error in results['errors']:
            messages.error(request, error)
    return redirect('/')

# Method to login with an existing user
def login(request):
    results = User.objects.login(request.POST)
    if results['valid']:
        request.session['login_id'] = results['user'].id
        return redirect('/book_reviews')
    else:
        for error in results['errors']:
            messages.error(request, error)
    return redirect('/')

# Method to logout of an existing acount
def logout(request):
    request.session.flush()
    return redirect('/') # redirect back to login page
