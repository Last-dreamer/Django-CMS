from django.http import HttpResponse
from django.shortcuts import redirect


def isUserAuthenticated(view_func):
    def wrapping_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapping_func


def allowed_users(allowed_user=None):
    if allowed_user is None:
        allowed_user = []

    def decorator(view_func):
        def wrapping_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group in allowed_user:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse('Sorry You Are Not allowed.....')
        return wrapping_func

    return decorator


def adminOnly(view_func):
    def wrapping_fun(request, *args, **kwargs):

        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

            if group == 'customer':
                return redirect('/user_page/' + str(request.user.customer.id))

            if group == 'admin':
                return view_func(request, *args, **kwargs)

    return wrapping_fun
