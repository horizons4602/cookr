from django.db import models


class Contact(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	message = models.TextField()

	def __str__(self):
		return self.name


class Newsletter(models.Model):
	email = models.EmailField(unique=True)

	def __str__(self):
		return self.email
