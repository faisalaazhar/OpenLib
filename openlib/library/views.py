from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.db import connection
from django.db import transaction
from .models import Book
import cx_Oracle

from .forms import RegisterForm, BookForm
from django.core.files.storage import FileSystemStorage

# Create your views here.


def index(request):
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM book')
        result = dictfetchall(cursor)
    finally:
        cursor.close()
    return render(request, 'library/home.html', {'result': result})


def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')

    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})


def userAccount(request):
    return render(request, "library/profile.html")


@transaction.atomic
def addBook(request):
    if request.method == "POST":
        if request.FILES:
            photo = request.FILES['photo']
            fss = FileSystemStorage()
            file = fss.save(photo.name, photo)
            file_url = fss.url(file)
            return render(request, 'library/addBook.html', {"file_url": file_url})
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/home')
    else:
        form = BookForm()

    return render(request, 'library/addBook.html', {"form": form})


def borrowBook(request, id):
    errorMessage = ''
    try:
        cursor = connection.cursor()
        result = cursor.callfunc('is_friday', bool)
        if (not result):
            count = cursor.callfunc('stock_count', float, [id])
            if count > 0:
                print(count)
        else:
            errorMessage += 'You cannot borrow books on friday.'
            return render(request, 'library/home.html', {"errorMessage": errorMessage})
    finally:
        cursor.close()
    return redirect("/profile")


@transaction.atomic
def deleteBook(request, id):
    book = Book.objects.get(book_id=id)
    book.delete()
    return redirect("/home")


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
