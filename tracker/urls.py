from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    path('transactions/<int:pk>/edit/', views.edit_transaction, name='edit_transaction'),
    path('transactions/<int:pk>/delete/', views.delete_transaction, name='delete_transaction'),
    path('categories/', views.categories, name='categories'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('account/', views.account_settings, name='account_settings'),
]
