from django import forms
from .models import Transaction, Category


class TransactionForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)
        self.fields['category'].empty_label = '— No Category —'

    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'transaction_type', 'category', 'payment_method', 'date', 'note']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Grocery shopping'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '0.00', 'step': '0.01', 'min': '0.01'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'note': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Optional note...', 'rows': 3}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'icon', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Food & Dining'}),
            'icon': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '🍔'}),
            'color': forms.TextInput(attrs={'class': 'form-input color-input', 'type': 'color'}),
        }


class FilterForm(forms.Form):
    PERIOD_CHOICES = [
        ('', 'All Time'), ('today', 'Today'), ('week', 'This Week'),
        ('month', 'This Month'), ('year', 'This Year'), ('custom', 'Custom Range'),
    ]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)

    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '🔍 Search...'}))
    transaction_type = forms.ChoiceField(choices=[('', 'All Types'), ('credit', 'Credit ↑'), ('debit', 'Debit ↓')], required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False, empty_label='All Categories', widget=forms.Select(attrs={'class': 'form-select'}))
    payment_method = forms.ChoiceField(choices=[('', 'All Methods')] + Transaction.PAYMENT_METHODS, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    period = forms.ChoiceField(choices=PERIOD_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}))
