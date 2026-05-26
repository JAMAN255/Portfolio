import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class ErrorLoggingMiddleware:
    """Middleware to log all exceptions and return helpful error responses."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            logger.exception(f"Error processing request {request.method} {request.path}", exc_info=e)
            return JsonResponse(
                {'error': str(e), 'type': type(e).__name__},
                status=500
            )
        return response
