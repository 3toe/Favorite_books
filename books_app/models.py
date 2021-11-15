from django.db import models
import re
import datetime

class LoginManager(models.Manager):
   def UserValidator(self, POSTData):
      errors = {}
      if len(POSTData['fname']) < 2 or not POSTData['fname'].isalpha():
         errors['fname'] = "First name should be only letters and at least 2 characters."
      if len(POSTData['lname']) < 2 or not POSTData['lname'].isalpha():
         errors['lname'] = "Last name should be only letters and at least 2 characters."
      EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
      if not EMAIL_REGEX.match(POSTData['email']):           
         errors['email'] = "Email address is required and with proper A@B.XYZ format."  
      if User.objects.filter(email=POSTData['email']):
         errors['emailreg'] = "The email address entered is already registered."
      if len(POSTData['password']) < 8:
         errors['passlength'] = "Password must be at least 8 characters."
      if POSTData['password'] != POSTData['p2']:
         errors['passmatch'] = "The password and confirmation password did not match."
      return errors

class User(models.Model):
   fname = models.CharField(max_length=255)
   lname = models.CharField(max_length=255)
   password = models.CharField(max_length=255)
   email = models.CharField(max_length=255)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   objects = LoginManager()

class BookManager(models.Manager):
   def BookValidator(self, POSTData):
      errors = {}
      if len(POSTData['title']) < 1:
         errors['title'] = "Please enter a title."
      if len(POSTData['desc']) < 5:
         errors['desc'] = "The description must be at least 5 characters long."
      return errors

   def BookUpdateVal(self,POSTData):
      errors = {}
      if len(POSTData['desc']) < 5:
         errors['desc'] = "The description must be at least 5 characters long."
      return errors

class Book(models.Model):
   title = models.CharField(max_length=255)
   desc = models.TextField()
   uploader = models.ForeignKey(User, related_name="uploaded_books", on_delete = models.CASCADE)
   faved_by = models.ManyToManyField(User, related_name="fav_books")
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   objects = BookManager()