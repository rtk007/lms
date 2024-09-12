from django.urls import reverse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login ,update_session_auth_hash,logout
from django.contrib.auth.hashers import check_password,make_password
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse

def index(request):
    return render(request, 'index.html')

def fpage(request):
    return render(request, 'fpage.html')

def apage(request):
    return render(request, 'apage.html')

def admin(request):
    return render(request, 'admin.html')

def queries(request):
    book_list = Book.objects.all()

    # Pass the data to the template
    return render(request, 'queries.html', {'book_list': book_list})

def mbooks(request):
    # Query all books from the database
    book_list = Book.objects.all()

    # Pass the data to the template
    return render(request, 'mbooks.html', {'book_list': book_list})

def musers(request):
    # Query all faculty members from the database
    faculty_list = Faculty.objects.all()

    # Pass the data to the template
    return render(request, 'musers.html', {'faculty_list': faculty_list})

def return_books(request):
    return render(request, 'return.html')


def addb(request):
    context = {
        "bookadd": BookForm()
    }
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()

   
    return render(request, 'addbooks.html', context)
def addu(request):
    context = {
        "useradd": FacultyForm()
    }
    if request.method == 'POST':
        f = FacultyForm(request.POST)
        if f.is_valid():
            f.save()
        else:
            f = FacultyForm()
    
    return render(request, 'addusers.html',context)

def delp(request, id):
    book = Book.objects.get(book_id=id)
    book.delete()
    return redirect('/Library/mbooks/')
def delu(request, id):
    user = Faculty.objects.get(id=id)
    user.delete()
    return redirect('/Library/musers/')

def inc(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.count += 1
    book.save()
    return redirect('/Library/mbooks/')
def dec(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.count > 0:  # Ensure the count doesn't go below zero
        book.count -= 1
        book.save()
    return redirect('/Library/mbooks/')
def issue(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
            user = request.user  # Assuming the user is authenticated

            if book.count > 0:
                # Update the user's borrowed books
                user.books_borrowed.add(book)
                user.save()

                # Decrease the book count
                book.count -= 1
                book.save()

                # Redirect to queries page
                return redirect('queries')

            else:
                # Handle the case where the book is not available
                return render(request, 'queries.html', {'books': Book.objects.all(), 'error': 'Book is not available.'})
                
        except Book.DoesNotExist:
            return render(request, 'queries.html', {'books': Book.objects.all(), 'error': 'Book not found.'})

    return redirect('queries')


def query(request):
    search_query = request.GET.get('search_query', '')

    if search_query:
        book_list = Book.objects.filter(
            book_name__icontains=search_query
        ) | Book.objects.filter(
            author__icontains=search_query
        ) | Book.objects.filter(
            book_id__icontains=search_query
        )
    else:
        book_list = Book.objects.all()  # Fetch all books if no search query

    return render(request, 'queries.html', {'book_list': book_list})


from django.contrib.auth import authenticate, login

def barcode_login(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty_id')
        try:
            faculty = Faculty.objects.get(id_number=faculty_id)
            # Authenticate using Faculty model fields
            if faculty:  # Assuming a match
                login(request, faculty)  # Log in the faculty member
                return redirect('index')  # Redirect to 'index' after successful login
            else:
                return render(request, 'index.html', {'error': 'Invalid ID'})
        except Faculty.DoesNotExist:
            return render(request, 'index.html', {'error': 'Invalid ID'})
    return render(request, 'index.html')
def verify_barcode(request):
    if request.method == 'POST':
        faculty_id = request.POST.get('faculty_id')
        
        # Check if the faculty ID exists in the Faculty table
        if Faculty.objects.filter(id_number=faculty_id).exists():
            # Redirect to fpage.html if valid
            return redirect('fpage')
        else:
            # Display an invalid address message
            return render(request, 'index.html', {'error': 'Invalid Faculty ID'})
    
    # Handle GET requests or other methods
    return redirect('index')
