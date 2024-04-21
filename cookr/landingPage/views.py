from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect
from .forms import ContactForm, NewsLetterForm


class Index(TemplateView):
	template_name = "landing/landingPage.html"

	def get(self, request, *args, **kwargs):
		form = NewsLetterForm()
		return self.render_to_response({'form': form})

	def post(self, request, *args, **kwargs):
		form = NewsLetterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('ThankYouTwo')
		return self.render_to_response({'form': form})


class About(TemplateView):
	template_name = "landing/about.html"


class Contact(TemplateView):
	template_name = "landing/contact.html"

	def get(self, request, *args, **kwargs):
		form = ContactForm()
		return self.render_to_response({'form': form})

	def post(self, request, *args, **kwargs):
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('ThankYou')
		return self.render_to_response({'form': form})


class Privacy(TemplateView):
	template_name = "landing/landingPP.html"


class TermsOfService(TemplateView):
	template_name = "landing/landingTOS.html"


class ThankYou(TemplateView):
	template_name = "landing/thankYou.html"


class ThankYouTwo(TemplateView):
	template_name = "landing/thankYou2.html"
