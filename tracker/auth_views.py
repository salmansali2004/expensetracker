from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile, Category


DEFAULT_CATEGORIES = [
    ('🍔', 'Food & Dining', '#f59e0b'),
    ('🚗', 'Transport', '#3b82f6'),
    ('🏠', 'Housing & Rent', '#8b5cf6'),
    ('💊', 'Health & Medical', '#ef4444'),
    ('🛍️', 'Shopping', '#ec4899'),
    ('🎬', 'Entertainment', '#06b6d4'),
    ('📚', 'Education', '#10b981'),
    ('💼', 'Business', '#6366f1'),
    ('💳', 'Bills & Utilities', '#f97316'),
    ('✈️', 'Travel', '#14b8a6'),
    ('💰', 'Salary / Income', '#22c55e'),
    ('🎁', 'Gifts', '#a855f7'),
]


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'dashboard'))
        messages.error(request, 'Invalid username or password.')
    return render(request, 'tracker/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        opening_balance = request.POST.get('opening_balance', '0') or '0'

        if not username or not password:
            messages.error(request, 'Username and password are required.')
        elif password != password2:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user, opening_balance=float(opening_balance))
            # Seed default categories
            for icon, name, color in DEFAULT_CATEGORIES:
                Category.objects.create(user=user, name=name, icon=icon, color=color)
            login(request, user)
            messages.success(request, f'Welcome to ExpenseIQ, {username}!')
            return redirect('dashboard')
    return render(request, 'tracker/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')
