from django.db import models

# Create your models here.


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(
        unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class Book(models.Model):
    book_id = models.FloatField(primary_key=True)
    title = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=200, blank=True, null=True)
    num_of_copies = models.FloatField()
    num_of_pages = models.FloatField()
    price = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True)
    book_description = models.CharField(max_length=3999, blank=True, null=True)
    cover_photo = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'book'


class BorrowBook(models.Model):
    borrow_id = models.FloatField(primary_key=True)
    user = models.ForeignKey(
        AuthUser, models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, blank=True, null=True)
    date_borrowed = models.DateField()
    date_returned = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'borrow_book'


class BookTransaction(models.Model):
    book_transaction_id = models.FloatField(primary_key=True)
    borrow = models.ForeignKey(
        'BorrowBook', models.DO_NOTHING, blank=True, null=True)
    borrow_cost = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True)
    fines = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'book_transaction'
