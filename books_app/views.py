from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# GET method returning the index page render
def index(request):
   return render(request, 'index.html')

# POST method for the registration, with an if for success/fail
def reg(request):
   # redirect if someone trying to bypass login:
   if request.method == 'GET':
      return redirect('/')
   # display errors if there are any and go back to login/reg page:
   errors = User.objects.UserValidator(request.POST)
   if len(errors) > 0:
      for key, value in errors.items():
         messages.error(request, value)
      return redirect('/')
   # hash password with bcrypt
   pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
   # create the user's db entry
   User.objects.create(fname = request.POST['fname'], lname = request.POST['lname'], password = pw_hash, email = request.POST['email'])
   user = User.objects.filter(email=request.POST['email'])
   # store user's name and id in session to access later:
   if user:
      logged_in = user[0]
      request.session['fname'] = logged_in.fname
      request.session['user_id'] = logged_in.id
   # access granted if all is well:
   return redirect('/books')

# POST method for the login, with an if for success/fail
def login(request):
   # redirect if someone trying to bypass login:
   if request.method == 'GET':
      return redirect('/')
   # check if email address entered exists in db, if not redirect to reg/login page:
   user = User.objects.filter(email=request.POST['email'])
   if user:
      logged_in = user[0]
      # if the user is found, check their hashed PW against the db hashed PW, error if needed:
      if bcrypt.checkpw(request.POST['password'].encode(), logged_in.password.encode()):
         request.session['fname'] = logged_in.fname
         request.session['user_id'] = logged_in.id
         # access granted if all is well:
         return redirect('/books')
   # error message if the login credentials aren't in the db
   messages.error(request, "Your username or password is incorrect.")
   return redirect('/')

# POST request to log user out upon log-out request.
def logout(request):
   # upon logout, flush the session and go back to reg / login page:
   request.session.flush()
   return redirect('/')

# GET method to render main page once user logs in or registers
def books(request):
   # redirect requests to the reg / login page if not logged-in:
   if not 'fname' in request.session:
      return redirect('/')
   # send down lists of users and wishes to render in the page via context dict:
   context = {
      "BookList" : Book.objects.order_by('title'),
      "U" : User.objects.get(id=request.session['user_id'])
   }
   return render(request, 'books.html', context)

# POST method to add a new book to the db
def AddBook(request):
   # redirect requests to the reg / login page if not logged-in:
   if not 'fname' in request.session:
      return redirect('/')
   # handle errors made by user when entering book info
   errors = Book.objects.BookValidator(request.POST)
   if len(errors) > 0:
      for key, value in errors.items():
         messages.error(request, value)
      return redirect('/books')
   user = User.objects.get(id=request.session['user_id'])
   newbook = Book.objects.create(title=request.POST['title'], desc=request.POST['desc'], uploader=user)
   newbook.faved_by.add(user)
   return redirect('/books')
   
# GET method to render individual book pages
def BookPage(request, book_id):
   # redirect requests to the reg / login page if not logged-in:
   if not 'fname' in request.session:
      return redirect('/')
   # context to pass relevant data into the template
   book = Book.objects.get(id=book_id)
   context = {
      "B" : book,
      "U" : User.objects.get(id=request.session['user_id']),
      "favers" : User.objects.filter(fav_books=book)
   }
   return render(request, 'bookpage.html', context)

# POST request to favorite a book
def fave(request, book_id):
   # redirect requests to the reg / login page if not logged-in:
   if not 'fname' in request.session:
      return redirect('/')
   # add user to the book's fave'rs
   book = Book.objects.get(id=book_id)
   user = User.objects.get(id=request.session['user_id'])
   book.faved_by.add(user)
   book.save()
   return redirect('/books')

# POST request to un-favorite a book
def unfave(request, book_id):
   # redirect requests to the reg / login page if not logged-in:
   if not 'fname' in request.session:
      return redirect('/')
   # add user to the book's fave'rs
   book = Book.objects.get(id=book_id)
   user = User.objects.get(id=request.session['user_id'])
   book.faved_by.remove(user)
   book.save()
   return redirect(f'/books/{book_id}')

# POST method to edit a book's info
def update(request, book_id):
   # redirect requests to the reg / login page if not logged-in:
   if not 'fname' in request.session:
      return redirect('/')
   if "del" in request.POST:
      Book.objects.get(id=book_id).delete()
      return redirect('/books')
   errors = Book.objects.BookUpdateVal(request.POST)
   if len(errors) > 0:
      for key, value in errors.items():
         messages.error(request, value)
      return redirect(f'/books/{book_id}')
   book = Book.objects.get(id=book_id)
   book.desc = request.POST['desc']
   book.save()
   return redirect('/books')