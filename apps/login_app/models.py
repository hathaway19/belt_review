# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt # For hashing passwords

class UserManager(models.Manager):
    # Creates acount after checking for valid information
    def register(self, postData):
        results = {'valid': True, 'errors': [], 'user': None}

        # Validations of user entered data (checks to see if fields are filled out)
        if not postData['name']:
            results['valid'] = False
            results['errors'].append("Please enter your name.")
        if not postData['alias']:
            results['valid'] = False
            results['errors'].append("Please enter your alias")
        if not postData['email']:
            results['valid'] = False
            results['errors'].append("Please enter your email address.")
        # Password needs to be 8 or more characters
        if not postData['password'] or len(postData['password']) < 8:
            results['valid'] = False
            results['errors'].append("Please enter a password with 8 or more characters.")
        # Checks to see if passwords are the same
        if postData['password'] != postData['confirm_password']:
            results['valid'] = False
            results['errors'].append("Please confirm that your two passwords match.")
        # Makes sure the email doesn't already exist in db
        if User.objects.filter(email=postData['email']).exists():
            results['valid'] = False
            results['errors'].append("There is already an existing user with that email address.")
        # Creates user if results are valid
        else:
            if results['valid']:
                # hash the password for security purposes
                hashed_password = bcrypt.hashpw(str(postData['password']), bcrypt.gensalt())
                new_user = User.objects.create(
                    name=postData['name'],
                    alias=postData['alias'],
                    email=postData['email'],
                    password=hashed_password
                )
                results['user'] = new_user
        return results

    # For logging in with an existing acount
    def login(self, postData):
        results = {'valid': True, 'errors': [], 'user': None}
        # Checks to see if user email exists in db
        try:
            results['user'] = User.objects.get(email=postData['email'])
        # Not a valid acount if the email doesn't exist
        except:
            results['valid'] = False
            results['errors'].append("There is no user with that email and password.")
            return results
        # If passwords don't match, not a valid acount
        if  str(results['user'].password) != bcrypt.hashpw(str(postData['password']), str(results['user'].password)):
            results['valid'] = False
            results['errors'].append("There is no user with that email and password.")
        # Return the results
        return results

# Model for user acounts
class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
