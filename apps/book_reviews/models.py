# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login_app.models import User

class BookManager(models.Manager):
    def empty_database(self):
        Review.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
    
    def validate(self, postData, user, results):
        if not postData['title']:
            results['valid'] = False
            results['errors'].append("Please enter a valid book title.")
        if postData['author_list'] == 'none':
            if not postData['new_author']:
                results['valid'] = False
                results['errors'].append("Please select an existing author or enter a new author.")
            else:
                if Author.objects.filter(name=postData['new_author']).exists():
                    results['valid'] = False
                    results['errors'].append("There's already an author with that name.")
                author = postData['new_author']
                results['new_author'] = True
        else:
            author = postData['author_list']
            results['new_author'] = False
        if len(postData['review']) < 2:
            results['valid'] = False
            results['errors'].append("Please fill out your review content.")
        return results
    
    def create_review(self, postData, user):
        results = {'valid': True, 'errors': [], 'new_author': True}
        results = self.validate(postData, user, results)

        if results['valid']:
            if results['new_author']:
                author = Author.objects.create(
                    name=postData['new_author']
                )
            else:
                author = Author.objects.get(name=postData['author_list'])
            if not Book.objects.filter(title=postData['title']).exists():
                book = Book.objects.create(
                    title=postData['title'],
                    author_id=author
                )
            else: 
                book = Book.objects.get(title=postData['title'])
            Review.objects.create(
                content=postData['review'],
                rating=int(postData['rating_select']),
                user_id=user,
                book_id=book
            )
        return results

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author_id = models.ForeignKey(Author)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class Review(models.Model):
    content = models.TextField(max_length=500)
    rating = models.PositiveSmallIntegerField()
    user_id = models.ForeignKey(User)
    book_id = models.ForeignKey(Book)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
