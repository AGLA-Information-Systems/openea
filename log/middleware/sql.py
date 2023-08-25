from django.conf import settings
from django.db import connection
from django.template import Template, Context

class SQLMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if settings.DEBUG and connection.queries:
            execution_sql_time = sum([float(q['time']) for q in connection.queries])        
            t = Template(
"""
{{nb_sql}} request{{nb_sql|pluralize:",s"}} : {{execution_sql_time}} second{{execution_sql_time|pluralize:",s"}}:
{% for sql in sql_log %}
[{{forloop.counter}}] {{sql.time}}s: {{sql.sql|safe}}
{% endfor %}         
""")
            print("---------------")
            print(t.render(Context({'sql_log':connection.queries,'nb_sql':len(connection.queries),'execution_sql_time':execution_sql_time})) )  
            print("---------------")


        return response
