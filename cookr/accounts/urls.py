from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
	path('register/', views.Register.as_view(), name='register'),
	path('account/', views.Account.as_view(), name='account'),
]