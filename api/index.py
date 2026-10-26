import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import app


class VercelPathMiddleware:
    """Restores the original request URL from Vercel rewrites."""

    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        from urllib.parse import parse_qs
        qs = parse_qs(environ.get('QUERY_STRING', ''))
        
        # 1. Prefer explicit __route query param injected by vercel.json
        if '__route' in qs and qs['__route']:
            target_path = qs['__route'][0]
            environ['PATH_INFO'] = target_path
            
        # 2. Check Vercel routing headers
        elif 'HTTP_X_MATCHED_PATH' in environ:
            environ['PATH_INFO'] = environ['HTTP_X_MATCHED_PATH']
        elif 'HTTP_X_VERCEL_MATCHED_PATH' in environ:
            environ['PATH_INFO'] = environ['HTTP_X_VERCEL_MATCHED_PATH']
        elif 'HTTP_X_FORWARDED_URI' in environ:
            environ['PATH_INFO'] = environ['HTTP_X_FORWARDED_URI'].split('?')[0]

        return self.wsgi_app(environ, start_response)


# Wrap Flask app with the middleware for Vercel WSGI
application = VercelPathMiddleware(app)
handler = application
app = application
