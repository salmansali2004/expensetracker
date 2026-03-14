from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from datetime import date, timedelta
import json

from .models import Transaction, Category, UserProfile
from .forms import TransactionForm, CategoryForm, FilterForm


def get_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user, defaults={'opening_balance': 0})
    return profile


def apply_filters(qs, form):
    if not form.is_valid():
        return qs
    d = form.cleaned_data
    if d.get('search'):
        qs = qs.filter(Q(title__icontains=d['search']) | Q(note__icontains=d['search']))
    if d.get('transaction_type'):
        qs = qs.filter(transaction_type=d['transaction_type'])
    if d.get('category'):
        qs = qs.filter(category=d['category'])
    if d.get('payment_method'):
        qs = qs.filter(payment_method=d['payment_method'])
    today = date.today()
    period = d.get('period')
    if period == 'today':
        qs = qs.filter(date=today)
    elif period == 'week':
        qs = qs.filter(date__gte=today - timedelta(days=7))
    elif period == 'month':
        qs = qs.filter(date__year=today.year, date__month=today.month)
    elif period == 'year':
        qs = qs.filter(date__year=today.year)
    elif period == 'custom':
        if d.get('date_from'):
            qs = qs.filter(date__gte=d['date_from'])
        if d.get('date_to'):
            qs = qs.filter(date__lte=d['date_to'])
    return qs


@login_required
def dashboard(request):
    profile = get_profile(request.user)
    txs = request.user.transactions.select_related('category')
    total_credits = txs.filter(transaction_type='credit').aggregate(s=Sum('amount'))['s'] or 0
    total_debits = txs.filter(transaction_type='debit').aggregate(s=Sum('amount'))['s'] or 0
    balance = profile.opening_balance + total_credits - total_debits

    today = date.today()
    month_tx = txs.filter(date__year=today.year, date__month=today.month)
    month_credits = month_tx.filter(transaction_type='credit').aggregate(s=Sum('amount'))['s'] or 0
    month_debits = month_tx.filter(transaction_type='debit').aggregate(s=Sum('amount'))['s'] or 0
    month_net = month_credits - month_debits

    recent = txs[:8]

    cat_data = list(
        txs.filter(transaction_type='debit', category__isnull=False)
        .values('category__name', 'category__color', 'category__icon')
        .annotate(total=Sum('amount'))
        .order_by('-total')[:7]
    )
    for item in cat_data:
        item['total'] = float(item['total'])

    monthly_data = []
    for i in range(5, -1, -1):
        d = (today.replace(day=1) - timedelta(days=i * 28)).replace(day=1)
        mc = txs.filter(date__year=d.year, date__month=d.month, transaction_type='credit').aggregate(s=Sum('amount'))['s'] or 0
        md = txs.filter(date__year=d.year, date__month=d.month, transaction_type='debit').aggregate(s=Sum('amount'))['s'] or 0
        monthly_data.append({'month': d.strftime('%b %y'), 'credits': float(mc), 'debits': float(md)})

    context = {
        'profile': profile,
        'balance': balance,
        'total_credits': total_credits,
        'total_debits': total_debits,
        'month_credits': month_credits,
        'month_debits': month_debits,
        'month_net': month_net,
        'recent': recent,
        'cat_data': json.dumps(cat_data),
        'monthly_data': json.dumps(monthly_data),
        'tx_count': txs.count(),
    }
    return render(request, 'tracker/dashboard.html', context)


@login_required
def transaction_list(request):
    txs = request.user.transactions.select_related('category')
    filter_form = FilterForm(request.user, request.GET or None)
    txs = apply_filters(txs, filter_form)

    total_credits = txs.filter(transaction_type='credit').aggregate(s=Sum('amount'))['s'] or 0
    total_debits = txs.filter(transaction_type='debit').aggregate(s=Sum('amount'))['s'] or 0

    context = {
        'transactions': txs,
        'filter_form': filter_form,
        'total_credits': total_credits,
        'total_debits': total_debits,
        'net': total_credits - total_debits,
        'count': txs.count(),
    }
    return render(request, 'tracker/transaction_list.html', context)


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            tx = form.save(commit=False)
            tx.user = request.user
            tx.save()
            messages.success(request, 'Transaction added!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(request.user)
        form.fields['date'].initial = date.today()
    return render(request, 'tracker/transaction_form.html', {'form': form, 'action': 'Add'})


@login_required
def edit_transaction(request, pk):
    tx = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST, instance=tx)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(request.user, instance=tx)
    return render(request, 'tracker/transaction_form.html', {'form': form, 'action': 'Edit', 'tx': tx})


@login_required
def delete_transaction(request, pk):
    tx = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        tx.delete()
        messages.success(request, 'Transaction deleted.')
        return redirect('transaction_list')
    return render(request, 'tracker/confirm_delete.html', {'tx': tx})


@login_required
def categories(request):
    cats = request.user.categories.all()
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=False)
            cat.user = request.user
            cat.save()
            messages.success(request, 'Category added!')
            return redirect('categories')
    return render(request, 'tracker/categories.html', {'cats': cats, 'form': form})


@login_required
def delete_category(request, pk):
    cat = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Category deleted.')
    return redirect('categories')


@login_required
def account_settings(request):
    profile = get_profile(request.user)
    if request.method == 'POST':
        ob = request.POST.get('opening_balance', '0') or '0'
        try:
            profile.opening_balance = float(ob)
            profile.save()
            messages.success(request, 'Account settings saved!')
        except ValueError:
            messages.error(request, 'Invalid balance value.')
        return redirect('account_settings')
    return render(request, 'tracker/account_settings.html', {'profile': profile})
