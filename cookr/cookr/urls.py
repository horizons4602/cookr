from django.contrib import admin
from django.urls import path
from landingPage.views import Index  # Ensure this import is correct

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL
    path('', Index.as_view(), name='Index'),  # Correct use of as_view() for class-based view
]
