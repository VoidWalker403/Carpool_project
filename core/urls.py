from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from accounts.views import signup
from django.contrib.auth import views as auth_views

def home(request):
    return HttpResponse("Carpool Project is Live 🚀")

urlpatterns = [
    path("", home, name="home"),

    # Admin
    path("admin/", admin.site.urls),

    # Auth pages
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", signup, name="signup"),
]