import random
import time
from django.shortcuts import render
from django.http import JsonResponse
from d07 import settings


USERNAME_VALIDITY_SECONDS = 42


def get_or_create_username(request):
    current_time = time.time()
    user_name = request.session.get('user_name')
    timestamp = request.session.get('user_name_timestamp')

    should_create_new = (
        not user_name or
        not timestamp or
        (current_time - timestamp) >= USERNAME_VALIDITY_SECONDS
    )

    if should_create_new:
        user_name = random.choice(settings.USER_NAMES)
        request.session['user_name'] = user_name
        request.session['user_name_timestamp'] = current_time

    return user_name


def ex(request):
    """Main homepage view."""
    user_name = get_or_create_username(request)
    return render(request, 'welcome.html', {'user_name': user_name})


def get_username(request):
    user_name = get_or_create_username(request)
    return JsonResponse({'user_name': user_name})
