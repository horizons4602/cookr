from django.db import models
from django.contrib.auth.models import User


def default_user():
    # Returns the first user, make sure a user exists or set it to a specific user ID
    return User.objects.first().id if User.objects.exists() else None


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', default=default_user)
    image_url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=255)
    time = models.CharField(max_length=100, default="0 min")
    calories = models.FloatField(default=0)
    fat = models.FloatField(default=0)
    carbs = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    ingredients = models.TextField(default="")
    site_url = models.URLField(blank=True, null=True)
    items = models.IntegerField(default=0)
    seen = models.IntegerField(default=0)

    def __str__(self):
        return self.name
