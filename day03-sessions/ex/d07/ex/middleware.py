import random
import time
from django.conf import settings

ANONYMOUS_SESSION_DURATION = 42

class AnonymousSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.session.get('username'):
            current_time = time.time()
            anonymous_username = request.session.get('anonymous_username')
            anonymous_timestamp = request.session.get('anonymous_timestamp')
            
            if not anonymous_username or not anonymous_timestamp or (current_time - anonymous_timestamp) >= ANONYMOUS_SESSION_DURATION:
                request.session['anonymous_username'] = random.choice(settings.USER_NAMES)
                request.session['anonymous_timestamp'] = current_time
        
        response = self.get_response(request)
        return response

