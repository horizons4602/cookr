from django.contrib import admin
from django.urls import path
from landingPage.views import Index, About, Contact, Privacy, TermsOfService, ThankYouTwo, ThankYou

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='Index'),
    path('about/', About.as_view(), name='About'),
    path('contact/', Contact.as_view(), name='Contact'),
    path('privacy_policy/', Privacy.as_view(), name='PrivacyPolicy'),
    path('terms_of_service/', TermsOfService.as_view(), name='TermsOfService'),
    path('thank_you/', ThankYou.as_view(), name='ThankYou'),
    path('thank_you_2/', ThankYouTwo.as_view(), name='ThankYouTwo'),
]
