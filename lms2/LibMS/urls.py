from django.urls import path
from .views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('fpage/', fpage, name='fpage'),
    path('apage/', apage, name='apage'),
    path('admin/', admin, name='admin'),
    path('queries/', queries, name='queries'),
    path('mbooks/', mbooks, name='mbooks'),
    path('musers/', musers, name='musers'),
    path('return/', return_books, name='return_books'),
    path('return/', return_book, name='return_book'),
    path('addbooks/', addb, name='addb'),
    path('addusers/', addu, name='addu'),
    path('mbooks/delete/<int:id>/', delp, name='del'),
    path('musers/<int:id>/', delu, name='delu'),
    path('mbooks/inc/<int:pk>/', inc, name='inc'),
    path('mbooks/dec/<int:pk>/', dec, name='dec'),
    path('queries/issue/', issue, name='issue'),
    path('queries/search/', query, name='query'),
    path('verify_barcode/<str:id_number>/', verify_barcode, name='verify_barcode')
,
]