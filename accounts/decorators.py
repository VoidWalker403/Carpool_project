from django.shortcuts import redirect

def driver_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/')
        if not request.user.groups.filter(name='Drivers').exists():
            return redirect('/passenger/')  # passengers can't access driver pages
        return view_func(request, *args, **kwargs)
    return wrapper

def passenger_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/login/')
        if not request.user.groups.filter(name='Passengers').exists():
            return redirect('/driver/')  # drivers can't access passenger pages
        return view_func(request, *args, **kwargs)
    return wrapper