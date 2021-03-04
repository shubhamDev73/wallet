from django.urls import path

from . import views

app_name = 'wallet'

urlpatterns = [
    path('create/', views.create, name='create'),
    path('balance/', views.balance, name='balance'),
    path('credit/', views.credit, name='credit'),
    path('debit/', views.debit, name='debit'),
]
