from django.urls import path
from . import views

urlpatterns = [
	path('', views.Index.as_view(), name='Index'),
	path('about/', views.About.as_view(), name='About'),
	path('contact/', views.Contact.as_view(), name='Contact'),
	path('privacy_policy/', views.Privacy.as_view(), name='PrivacyPolicy'),
	path('terms_of_service/', views.TermsOfService.as_view(), name='TermsOfService'),
	path('thank_you/', views.ThankYou.as_view(), name='ThankYou'),
	path('thank_you_2/', views.ThankYouTwo.as_view(), name='ThankYouTwo'),
]
