from django.http import HttpResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
import base64

AUTH_TEMPLATE = """ <html> <title>Authentication Required</title> <body> Sorry, we're not ready for you yet. </body> </html> """

class BasicAuthMiddleware(MiddlewareMixin):
    def unauthed(self):
        response = HttpResponse(AUTH_TEMPLATE, content_type="text/html")
        response['WWW-Authenticate'] = 'Basic realm="Development"'
        response.status_code = 401
        return response

    def process_request(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            return self.unauthed()
        else:
            authentication = request.META['HTTP_AUTHORIZATION']
            (auth_method, auth) = authentication.split(' ', 1)
            if 'basic' != auth_method.lower():
                return self.unauthed()
            auth = base64.b64decode(auth.strip()).decode('utf-8')
            username, password = auth.split(':', 1)
            if (
                    username == settings.BASICAUTH_USERNAME and
                    password == settings.BASICAUTH_PASSWORD
            ):
                return self.get_response(request)

            return self.unauthed()