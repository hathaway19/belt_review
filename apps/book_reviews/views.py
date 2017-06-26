# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from ..login_app.models import User
from django.db.models import Max
from models import Book, Author, Review

def index(request):
    # Book.objects.empty_database()
    try:
        current_user = User.objects.get(id=request.session['login_id'])
    except:
        print "User is not logged in"
        return redirect(reverse('login_app:logout'))

    all_authors = Author.objects.all()
    all_books = Book.objects.all()
    all_reviews = Review.objects.all()

    recent_reviews = Review.objects.order_by('-created_at')[:5]

    recent = []
    for review in recent_reviews:
        recent.append(review)

    context = {
        'all_books': all_books,
        'all_reviews': all_reviews,
        'current_user': current_user,
        'recent': recent
    }
    print "********************* Books ***********************"
    for book in all_books:
        print "*************** New Book ************************"
        print book.title, book.author_id.name
    print "********************* Reviews ***********************"
    for review in all_reviews:
        print review.book_id.title, review.book_id.author_id.name, review.user_id.name

    
    return render(request, 'book_reviews/index.html', context)

# Page that allows user to fill in information to add a new review
def add_review_page(request):
    all_authors = Author.objects.all()
    context = {
        'all_authors': all_authors
    }
    return render(request, 'book_reviews/add_review_page.html', context)

# Called when trying to create a new review
def create_review(request):
    try:
        # get the user trying to make the review
        current_user = User.objects.get(id=request.session['login_id'])
    except:
        # Logs out if user id can't be found
        print "User is not logged in"
        return redirect(reverse('login_app:logout'))

    # Gets the results
    results = Book.objects.create_review(request.POST, current_user)
    # If the review was successfully created, go to the home page
    if results['valid']:
        return redirect(reverse('book_reviews:index'))
    # If not, print errors and stay on page
    else:
        for error in results['errors']:
            messages.error(request, error)
        return redirect(reverse('book_reviews:add_review'))

# Page to look at an individual book and see all reviews pertaining to it
def show_book(request, id):
    # Get the current user, if not, log out
    try:
        user = User.objects.get(id=request.session['login_id'])
    except:
        print "User is not logged in"
        return redirect(reverse('login_app:logout'))
    # Gets the current book 
    try:
        book = Book.objects.get(id=id)
    # Go back to homescreen if you couldn't obtain book
    except:
        print "No book matches the id", id
        return redirect(reverse('book_reviews:index'))

    # All reviews dealing with book in question
    books_reviews = Review.objects.filter(book_id=book)
    context = {
        'user': user,
        'book': book,
        'books_reviews': books_reviews
    }
    return render(request, 'book_reviews/show_book.html', context)

def delete_review(request, id):
    try:
        user = User.objects.get(id=request.session['login_id'])
    except:
        print "User is not logged in"
        return redirect(reverse('login_app:logout'))
    try:
        review = Review.objects.get(id=id)
    except:
        return redirect(reverse('book_reviews:index'))

    review.delete()
    return redirect(reverse('book_reviews:index'))

def show_user(request, id):
    try:
        user = User.objects.get(id=id)
    except:
        return redirect(reverse('book_reviews:index'))

    their_reviews = Review.objects.filter(user_id=user)
    num_of_reviews = len(their_reviews)
    context = {
        'user': user,
        'their_reviews': their_reviews,
        'num_of_reviews': num_of_reviews
    }
    return render(request, 'book_reviews/show_user.html', context)