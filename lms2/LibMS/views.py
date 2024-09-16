from django.urls import reverse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login ,update_session_auth_hash,logout
from django.contrib.auth.hashers import check_password,make_password
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from django.utils import timezone

def index(request):
    return render(request, 'index.html')

def fpage(request):
    faculty_name = request.session.get('faculty_name', 'Guest')
    faculty_id = request.session.get('faculty_id', None)
    # Render the fpage template and pass the faculty name
    return render(request, 'fpage.html', {'faculty_name': faculty_name, 'faculty_id': faculty_id})

def apage(request):
    return render(request, 'apage.html')

def admin(request):
    return render(request, 'admin.html')

def queries(request):
    faculty_name = request.session.get('faculty_name', 'Guest')
    faculty_id = request.session.get('faculty_id', None)

    # Pass the data to the 'queries.html' template along with the books list
    book_list = Book.objects.all()
    return render(request, 'queries.html', {
        'book_list': book_list,
        'faculty_name': faculty_name,
        'faculty_id': faculty_id
    })

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
    faculty_id = request.session.get('faculty_id', None)
    faculty_name = request.session.get('faculty_name', None)

    if faculty_id is None:
        # Redirect to index if faculty is not logged in
        return redirect('index')

    try:
        # Get the faculty object based on the session id
        faculty = Faculty.objects.get(id_number=faculty_id)

        # Get all issued books for this faculty
        issued_books = BookIssue.objects.filter(faculty=faculty)

        # Pass the issued books to the template context
        context = {
            'faculty_name': faculty.name,
            'faculty_id': faculty.id_number,
            'issued_books': issued_books,
        }
        
        return render(request, 'return.html', context)
    
    except Faculty.DoesNotExist:
        # Redirect to login if the faculty doesn't exist
        return redirect('index')

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
        faculty_id = request.session.get('faculty_id')  # Get faculty ID from session

        try:
            book = Book.objects.get(book_id=book_id)
            faculty = Faculty.objects.get(id_number=faculty_id)

            if book.count > 0:
                # Create a new BookIssue entry
                BookIssue.objects.create(
                    faculty=faculty,
                    book=book,
                    issue_date=timezone.now(),  # Record the current date as issue date
                    due_date=timezone.now() + timezone.timedelta(days=14)  # Set due date, e.g., 14 days later
                )

                # Reduce the book count
                book.count -= 1
                book.save()

                # Create a new entry in BookHistory to track the issuance of the book
                BookHistory.objects.create(
                    faculty=faculty,
                    book=book,
                    action=1,  # 1 for Issued
                    date_time=timezone.now()  # Record the current timestamp
                )

                # Success message
                messages.success(request, f"Book '{book.book_name}' issued successfully!")
                return redirect('queries')
            else:
                # If the book is not available
                messages.error(request, "Book is not available.")
                return redirect('queries')

        except Book.DoesNotExist:
            messages.error(request, "Book not found.")
            return redirect('queries')
        except Faculty.DoesNotExist:
            messages.error(request, "Faculty not found.")
            return redirect('index')  # Redirect to login if faculty is not found

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

# views.py

def verify_barcode(request, id_number):
    if request.method == 'POST':
        try:
            # Get the faculty object based on the scanned ID number
            faculty = Faculty.objects.get(id_number=id_number)
            
            # Store faculty name and ID in the session
            request.session['faculty_name'] = faculty.name
            request.session['faculty_id'] = faculty.id_number
            
            # Redirect to fpage.html if valid
            return redirect(reverse('fpage'))
        
        except Faculty.DoesNotExist:
            # Display error if the ID is invalid
            return render(request, 'index.html', {'error': 'Invalid Faculty ID'})
    
    return redirect('index')



def return_book(request):
    book_id = request.POST.get('book_id')  # Get book_id from the form
    faculty_id = request.session.get('faculty_id')  # Get faculty_id from the session

    # Check if faculty_id exists in session
    if not faculty_id:
        messages.error(request, "Session has expired or faculty ID is missing.")
        return redirect('/Library/login/')

    try:
        # Debug: Print the book_id and faculty_id values
        print(f"Book ID: {book_id}, Faculty ID: {faculty_id}")

        # Fetch the specific BookIssue instance to delete
        book_issue = BookIssue.objects.get(book__id=book_id, faculty__id_number=faculty_id)

        # Delete the BookIssue instance
        book_issue.delete()

        # Update the book count after deletion
        book = book_issue.book
        book.count += 1
        book.save()

        # Redirect after successful deletion
        return redirect('/Library/return/')

    except BookIssue.DoesNotExist:
        # Handle case where no BookIssue record exists
        messages.error(request, "The book issue record does not exist.")
        return redirect('/Library/return/')
    
    except Exception as e:
        # Handle any other exceptions and log the error
        messages.error(request, f"An error occurred: {e}")
        return redirect('/Library/return/')
