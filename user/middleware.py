from .models import UserActionLog


class UserActionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            UserActionLog.objects.create(
                user=request.user,
                path=request.path,
                method=request.method,
            )

        return response
