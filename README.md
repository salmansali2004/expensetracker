# 💸 ExpenseIQ — Multi-User Expense Tracker

A full-featured Django expense tracker with user authentication, where each user
has completely isolated, private financial data.

---

## 🚀 Quick Setup

### 1. Install Django
```bash
pip install django
```

### 2. Run Migrations
```bash
cd expense_tracker
python manage.py makemigrations tracker
python manage.py migrate
```

### 3. Create an Admin (optional)
```bash
python manage.py createsuperuser
```

### 4. Start the Server
```bash
python manage.py runserver
```

### 5. Open in Browser
```
http://127.0.0.1:8000/
```

---

## 👤 User Flow

| Page | URL | Description |
|------|-----|-------------|
| Register | `/register/` | Create new account — auto-seeds 12 categories |
| Login | `/login/` | Sign in to your account |
| Dashboard | `/` | Overview with charts & stats |
| Transactions | `/transactions/` | Full list with filters |
| Add | `/transactions/add/` | Add credit or debit |
| Categories | `/categories/` | Manage your categories |
| Account | `/account/` | Set opening balance |
| Admin | `/admin/` | Django admin panel |

---

## ✨ Features

### Authentication
- ✅ Register / Login / Logout
- ✅ Each user's data is completely private
- ✅ Password validation (min 6 chars)
- ✅ Redirect to login for protected pages

### Transactions
- ✅ Add Credits (money in) and Debits (money out)
- ✅ Title, amount, date, category, payment method, note
- ✅ Edit and delete any transaction
- ✅ Payment methods: Cash, Card, UPI, Bank Transfer, Cheque, Other

### Filters & Search
- ✅ Search by title or note
- ✅ Filter by type (credit/debit)
- ✅ Filter by category
- ✅ Filter by payment method
- ✅ Time periods: Today, This Week, This Month, This Year, Custom Range

### Dashboard
- ✅ Current balance (opening + credits − debits)
- ✅ Total credits & debits
- ✅ This month's summary
- ✅ Monthly trend bar chart (last 6 months)
- ✅ Spending by category donut chart
- ✅ Recent activity feed

### Categories
- ✅ 12 default categories auto-created on registration
- ✅ Add custom categories with emoji icon + color
- ✅ Per-user categories (not shared)

### Account
- ✅ Set opening balance
- ✅ View account summary stats
- ✅ Profile info display

---

## 📁 Project Structure

```
expense_tracker/
├── manage.py
├── requirements.txt
├── expense_tracker/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── tracker/                  # Main app
    ├── models.py             # Transaction, Category, UserProfile
    ├── views.py              # Dashboard, list, add, edit, delete
    ├── auth_views.py         # Login, Register, Logout
    ├── forms.py              # TransactionForm, CategoryForm, FilterForm
    ├── urls.py
    ├── admin.py
    └── templates/tracker/
        ├── base.html         # Sidebar layout + styling
        ├── login.html
        ├── register.html
        ├── dashboard.html    # Charts (Chart.js)
        ├── transaction_list.html
        ├── transaction_form.html
        ├── confirm_delete.html
        ├── categories.html
        └── account_settings.html
```

---

## 🎨 Design

- **Dark theme** with purple/green/red accent palette
- **Syne** display font + **DM Mono** for numbers
- Fully responsive sidebar layout
- Chart.js for bar + donut charts (loaded from CDN)
- No external CSS framework — pure custom CSS

---

## 🔐 Security Notes

For production, update `settings.py`:
```python
SECRET_KEY = 'your-real-secret-key-here'
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```
