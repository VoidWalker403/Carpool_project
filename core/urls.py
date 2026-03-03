from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("Carpool Project is Live 🚀")
from django.contrib.auth import views as auth_views

urlpatterns = [
  path("", home),
  path("admin/", admin.site.urls),
]