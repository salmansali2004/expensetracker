from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default='💰')
    color = models.CharField(max_length=20, default='#7c3aed')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
        unique_together = ['user', 'name']


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    date = models.DateField(default=timezone.now)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} | {self.get_transaction_type_display()} - {self.title} - ₹{self.amount}"

    class Meta:
        ordering = ['-date', '-created_at']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency_symbol = models.CharField(max_length=5, default='₹')

    def get_balance(self):
        from django.db.models import Sum
        credits = self.user.transactions.filter(transaction_type='credit').aggregate(s=Sum('amount'))['s'] or 0
        debits = self.user.transactions.filter(transaction_type='debit').aggregate(s=Sum('amount'))['s'] or 0
        return self.opening_balance + credits - debits

    def __str__(self):
        return f"{self.user.username}'s profile"
