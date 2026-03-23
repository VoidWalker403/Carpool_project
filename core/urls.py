from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from accounts.views import signup
from django.contrib.auth import views as auth_views
from accounts.views import passenger_dashboard, driver_dashboard
from django.views.generic import RedirectView
from accounts.views_redirect import post_login_redirect

def home(request):
    return HttpResponse("Carpool Project is Live 🚀")

urlpatterns = [
    path("", RedirectView.as_view(url="/login/", permanent=False)),

    # Admin
    path("admin/", admin.site.urls),

    # Auth pages
    path("login/", auth_views.LoginView.as_view(
    template_name="registration/login.html",
    next_page="/post-login/"), name="login"),
    path("post-login/", post_login_redirect, name="post_login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", signup, name="signup"),
    path("passenger/", passenger_dashboard, name="passenger_dashboard"),
    path("driver/", driver_dashboard, name="driver_dashboard"),
    path('', include('accounts.urls')),
    path('api/trips/', include('trips.urls')),
    path('accounts/', include('allauth.urls')),
    
]
