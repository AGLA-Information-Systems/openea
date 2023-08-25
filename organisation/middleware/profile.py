import traceback

class ActiveProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            if not hasattr(request.user, 'active_profile'):
                request.user.active_profile = None
            if not hasattr(request.user, 'organisation'):
                request.user.organisation = None
            if request.user.active_profile is None:
                try:
                    active_profile = request.user.profiles.get(is_active=True)
                    request.user.active_profile = active_profile
                    request.user.organisation = active_profile.organisation
                except:
                    traceback.print_exc()
            
            #request.user.timezone = evaluate_tz()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
