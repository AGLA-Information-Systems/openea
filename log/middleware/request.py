import threading

local_thread = threading.local()

def get_request():
    return getattr(local_thread, 'request', None)

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        local_thread.request = request
        return self.get_response(request)