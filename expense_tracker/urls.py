from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tracker import auth_views as custom_auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', custom_auth.login_view, name='login'),
    path('register/', custom_auth.register_view, name='register'),
    path('logout/', custom_auth.logout_view, name='logout'),
    path('', include('tracker.urls')),
]
