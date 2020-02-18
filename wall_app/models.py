# Create your models here.
from django.db import models
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
import bcrypt

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        
        # FN more than 2
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters"

        # LN more than 2
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters"
        
        # Email Valid
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"

        # Unique email
        given_email = postData['email']
        temp = User.objects.filter(email=given_email)
        if len(temp) != 0:
            errors['email'] = 'Invalid email address'

        # Date must be valid and be before today
        today = datetime.now()
        today_minus_13 = today + relativedelta(years=-13)
        if len(postData['birthdate']) == 0:
            errors['birthdate'] = 'Release date must be entered properly'
        elif (datetime.strptime(postData['birthdate'], "%Y-%m-%d").date() >= today.date()):
            errors['birthdate'] = 'Date must be before today'
        elif (datetime.strptime(postData['birthdate'], "%Y-%m-%d").date() >= today_minus_13.date()):
            errors['birthdate'] = 'You must be 13 years or older to use this'

        # PW matches
        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Passwords don't match"

        # PW longer than 8
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        
        return errors

    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['login_email'])
        # If no matching user found
        if len(user) != 1:
            errors['login_email']='Invalid email address or password 1'
        # If matching user found, but...
        else:
            # If password check returns false
            if bcrypt.checkpw(postData['login_password'].encode(), user[0].password.encode()) == False:
                errors['login_email']='Invalid email address or password 2'
        
        return errors

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    birthdate=models.DateField()
    # messages = list of messages
    # comments = list of comments
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
class MessageManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        # Message blank
        if len(postData['message_text']) < 1:
            errors['message_text'] = "Message was blank"
        
        return errors

class Message(models.Model):
    message_user = models.ForeignKey(User, related_name="messages", on_delete = models.CASCADE)
    message=models.TextField()
    # comments = list of comments
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()
    
class Comment(models.Model):
    parent_message = models.ForeignKey(Message, related_name="comments", on_delete = models.CASCADE)
    comment_user = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
    comment=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    