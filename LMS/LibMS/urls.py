from django.urls import path
from .views import *


urlpatterns = [
    
    path('index/', barcode_login, name='index'),
    path('fpage/',  fpage, name='fpage'),
    path('apage/', apage, name='apage'),
    path('admin/', admin, name='admin'),
    path('queries/', queries, name='queries'),
    path('mbooks/', mbooks, name='mbooks'),
    path('musers/', musers, name='musers'),
    path('return/', return_books, name='return_books'),
    path('addbooks/', addb, name='addb'),
    path('addusers/', addu, name='addu'),
    path('Library/mbooks/delete/<int:id>/', delp, name='del'),
    path('Library/musers/<int:id>/', delu, name='delu'),
    path('Library/mbooks/inc/<int:pk>/', inc, name='inc'),
    path('Library/mbooks/dec/<int:pk>/', dec, name='dec'),
    path('queries/issue/', issue, name='issue'),
    path('queries/search/', query, name='query'),
    path('Library/verify_barcode/<str:id_number>', verify_barcode, name='verify_barcode'),



]
