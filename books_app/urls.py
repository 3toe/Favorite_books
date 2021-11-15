from django.urls import path     
from . import views

urlpatterns = [
   # GET method returning the index page render
   path('', views.index),
   # POST method for the registration
   path('reg',  views.reg),
   # POST method for the login
   path('login',  views.login),
   # GET method logging the user out
   path('logout',  views.logout),
   # GET method to render main page once user logs in or registers
   path('books', views.books),
   # GET to redirect dangling "/"
   path('books/', views.books),
   # POST method to add a book to the db
   path('AddBook', views.AddBook),
   # GET method to render individual book pages
   path('books/<int:book_id>', views.BookPage),
   # POST method to favorite a book
   path('books/fave/<int:book_id>', views.fave),
   # POST method to remove a book from favorites
   path('books/unfave/<int:book_id>', views.unfave),
   # POST method to process editing/deleting
   path('books/update/<int:book_id>', views.update)
]