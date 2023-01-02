from django.urls import path
from . import views

app_name = "library"

urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.index, name="index"),
    path('signup', views.sign_up, name="signup"),
    path('profile', views.userAccount, name="userAccount"),
    path('addBook', views.addBook, name="addBook"),
    path('delete/<int:id>', views.deleteBook, name="deleteBook"),
    path('borrow/<int:id>', views.borrowBook, name="borrowBook"),
]
