# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        #check first and last name
        if len(post_data['first_name']) < 3:
            errors['first_name'] = "User first name should be longer than 3 characters"
        if len(post_data['last_name']) < 3:
            errors['last_name'] = "User last name should be longer than 3 characters"
        # check email validation
        if not 'email' in errors and not re.match(EMAIL_REGEX, post_data['email']):
            errors['email'] = "Email is invalid"
        else:
            if len(self.filter(email = post_data['email'])) > 1:
                errors['email'] = 'Email address is already in use'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()