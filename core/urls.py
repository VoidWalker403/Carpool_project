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
from accounts.views import signup
path("signup/", signup, name="signup"),
urlpatterns = [
    path("login/", ...),
    path("signup/", signup),
    path("admin/", admin.site.urls),
]