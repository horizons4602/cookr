from django.db import models


class Contact(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	message = models.TextField()


class Newsletter(models.Model):
	email = models.EmailField()
