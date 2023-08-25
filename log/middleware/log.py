from django.utils import timezone
import traceback
from log.models import Log


class ExecutionTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = request.META.get('REMOTE_ADDR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[-1].strip()

        request.timestamp = timezone.now()
        request.ip_address = ip_address
        request.log_object = []
        
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        executed_view = "Unknown"
        if hasattr(request, 'view') and request.view is not None:
            executed_view = str(request.view.__class__.__name__)

        execution_time = "Unknown"
        if hasattr(request, 'timestamp') and request.timestamp is not None:
            execution_time = timezone.now() - request.timestamp

        log_detail = []
        if hasattr(request, 'log_object') and isinstance(request.log_object, list):
            for log_event in request.log_object:
                try:
                    log_event = Log.objects.create(
                        source=executed_view + ':' + str(log_event.get('source')),
                        target=log_event.get('target'),
                        uri=request.build_absolute_uri,
                        ip_address=request.ip_address,
                        details=log_detail,
                        user=request.user,
                        organisation=log_event.get('organisation'),
                        timestamp=request.timestamp
                    )
                    log_event.save()
                except Exception as e:
                    traceback.print_exc()

        print ("%s : %s s " % (executed_view, execution_time))

        return response
