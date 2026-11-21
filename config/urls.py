from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/",include('accounts.urls')),
    path("wb/",include('core.urls')),
    path("/",include('home.urls')),
]
