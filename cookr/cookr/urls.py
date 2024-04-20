from django.contrib import admin
from django.urls import path, include
from landingPage.views import Index, About, Contact, Privacy, TermsOfService, ThankYouTwo, ThankYou

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landingPage.urls')),
    path('', include('accounts.urls')),
]
