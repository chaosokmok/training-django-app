from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps
from .models import Profile


def role_required(*allowed_roles):
   def decorator(view_func):
       @wraps(view_func)
       def wrapper(request, *args, **kwargs):
           if not request.user.is_authenticated:
               return redirect('login')  # ถ้ายังไม่ได้ล็อกอิน ให้ไปหน้า login
           try:
               profile = request.user.profile
               if profile.user_type in allowed_roles:
                   return view_func(request, *args, **kwargs)
               else:
                   return HttpResponseForbidden("You don't have permission to access this page.")
           except Profile.DoesNotExist:
               return HttpResponseForbidden("Profile not found.")
       return wrapper
   return decorator