from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def post_login_redirect(request):
    user = request.user

    if user.is_superuser or user.is_staff:
        return redirect("/admin/")

    if user.groups.filter(name="Drivers").exists():
        return redirect("/driver/")

    return redirect("/passenger/")