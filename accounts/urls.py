# accounts/urls.py
from django.urls import path
from .views import SignUpView
from. import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('account/update/', views.update_balance, name='update_balance'),
]

from django.contrib.auth import views as auth_views
# path('', auth_views.LogoutView.as_view(), name='logout'),