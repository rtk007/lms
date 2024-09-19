from django.urls import reverse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login ,logout
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def index(request):
    return render(request, 'index.html')

def fpage(request):
    faculty_name = request.session.get('faculty_name', 'Guest')
    faculty_id = request.session.get('faculty_id', None)
    # Render the fpage template and pass the faculty name
    return render(request, 'fpage.html', {'faculty_name': faculty_name, 'faculty_id': faculty_id})

def apage(request):
    if request.method == 'POST':
        username = request.POST['admin_id']
        password = request.POST['password']

        # Check if the username and password match a superuser
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            # Log the user in and redirect to the admin dashboard
            login(request, user)
            return redirect('/Library/admin')
        else:
            # Return an error message if credentials are invalid
            return HttpResponse("Invalid login credentials, or not a superuser.")

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
                issued_date = timezone.now()
                due_date = issued_date + timedelta(days=14)

                # Create a new BookIssue entry
                BookIssue.objects.create(
                    faculty=faculty,
                    book=book,
                    issue_date=issued_date,
                    due_date=due_date
                )

                # Reduce the book count
                book.count -= 1
                book.save()

                # Record the book history
                BookHistory.objects.create(
                    faculty=faculty,
                    book=book,
                    action=1,
                    date_time=timezone.now()
                )

                # Send email notification
                subject = 'Book Issued Successfully'
                html_message = render_to_string('emails/issue_notification.html', {
                    'faculty': faculty,
                    'book': book,
                    'issued_date': issued_date,
                    'return_date': due_date,
                })
                plain_message = strip_tags(html_message)
                from_email = 'ratikkrishna15@gmail.com'
                to_email = faculty.email

                send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

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

def return_book(request, id):
    try:
        # Get the BookIssue record that matches the book_id and the faculty
        book_issue = BookIssue.objects.filter(book_id=id)
        book = Book.objects.get(book_id=id)
        faculty_id= request.session.get('faculty_id')
        faculty = Faculty.objects.get(id_number=faculty_id)
        # Increment the book count since it is being returned
        book.count += 1
        book.save()
        BookHistory.objects.create(
            faculty=faculty,
            book=book,
            action=0,  # 1 for issue, 0 for return
            date_time=timezone.now()
        )
        # Delete the book issue entry as the book is returned
        book_issue.delete()
        subject = 'Book Returned Successfully'
        html_message = render_to_string('emails/return_notification.html', {'faculty': faculty, 'book': book})
        plain_message = strip_tags(html_message)
        from_email = 'ratikkrishna15@gmail.com'
        to_email = faculty.email

        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)


        # Display success message and redirect to the return page
        messages.success(request, "Book returned successfully!")
        return redirect('return_books')
    
    except BookIssue.DoesNotExist:
        # If the book issue record does not exist
        messages.error(request, "Book issue record not found.")
        return redirect('return_books')

    except Book.DoesNotExist:
        # If the book does not exist
        messages.error(request, "Book not found.")
        return redirect('return_books')

    except Faculty.DoesNotExist:
        # If the faculty does not exist
        messages.error(request, "Faculty not found.")
        return redirect('index')  # Redirect to login if faculty is not found
    
def admin_logout(request):
    request.session.flush()
    logout(request)  # Log out the user
    return redirect('/Library/index') 
def user_logout(request):
    request.session.flush()
    logout(request)  # Log out the user
    return redirect('/Library/index') 
def bookissue(request):
    # Retrieve all book issues from the database
    book_issues = BookIssue.objects.all().select_related('faculty', 'book')
    
    # Pass the data to the template
    context = {
        'book_issue_list': book_issues
    }
    return render(request, 'book_issue.html', context)
def bookhistory(request):
    # Retrieve all book histories from the database
    book_histories = BookHistory.objects.all().select_related('faculty', 'book')
    
    # Pass the data to the template
    context = {
        'book_history_list': book_histories
    }
    return render(request, 'book_history.html', context)
