from django.db import models
from django.utils import timezone

class Book(models.Model):
    book_id = models.CharField(max_length=10, primary_key=True)
    book_name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    count = models.IntegerField()
    rack = models.CharField(max_length=50)
    shelf = models.CharField(max_length=50)

    def __str__(self):
        return self.book_name

class Faculty(models.Model):
    name = models.CharField(max_length=200)
    id_number = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, default="null")
    is_first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class BookIssue(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()  # You can set this dynamically based on borrowing policies

    def __str__(self):
        return f"{self.faculty.name} - {self.book.book_name}"
class BookHistory(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    action = models.IntegerField(choices=[(1, 'Issued'), (0, 'Returned')])
    date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.faculty.name} - {self.book.title} - {'Issued' if self.action == 1 else 'Returned'}"