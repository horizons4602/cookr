from django.shortcuts import render
from django.views.generic import TemplateView


class Index(TemplateView):
	template_name = "landing/landingPage.html"


class About(TemplateView):
	template_name = "landing/about.html"


class Contact(TemplateView):
	template_name = "landing/contact.html"


class Privacy(TemplateView):
	template_name = "landing/landingPP.html"


class TermsOfService(TemplateView):
	template_name = "landing/landingTOS.html"


class ThankYou(TemplateView):
	template_name = "landing/thankYou.html"


class ThankYouTwo(TemplateView):
	template_name = "landing/thankYou2.html"
