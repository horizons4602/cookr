from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landingPage.urls')),
    path('', include('accounts.urls')),
    path('demo/', include('recipes.urls'))
]
