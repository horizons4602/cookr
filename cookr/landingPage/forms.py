from django import forms
from .models import Contact, Newsletter


class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = ['name', 'email', 'message']
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'email': forms.EmailInput(attrs={'class': 'form-control'}),
			'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
		}


class NewsLetterForm(forms.ModelForm):
	class Meta:
		model = Newsletter
		fields = ['email']
		widgets = {
			'email': forms.EmailInput(attrs={'class': 'form-control'}),
		}
