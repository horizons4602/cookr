from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user=True, next_page=reverse_lazy('main')), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('account/', views.Account.as_view(), name='account'),
]