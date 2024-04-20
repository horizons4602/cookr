from django.urls import path
from . import views

urlpatterns = [
	path('saved/', views.Saved.as_view(), name='saved'),
]
