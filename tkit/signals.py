from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from threading import local

_user_request = local()

def get_current_request():
    return getattr(_user_request, 'request', None)

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user_request.request = request
        response = self.get_response(request)
        return response
