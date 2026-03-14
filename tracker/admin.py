from django.contrib import admin
from .models import Transaction, Category, UserProfile

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'amount', 'transaction_type', 'category', 'payment_method', 'date']
    list_filter = ['transaction_type', 'payment_method', 'date']
    search_fields = ['title', 'note', 'user__username']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'icon', 'color']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'opening_balance', 'currency_symbol']
