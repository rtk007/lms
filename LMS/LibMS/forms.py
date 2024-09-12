from django.contrib.auth.hashers import check_password
from django import forms
from .models import *

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_id', 'book_name', 'author', 'count', 'rack', 'shelf']
        
class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name', 'id_number', 'username', 'password', 'email']
