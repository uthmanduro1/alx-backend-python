from datetime import datetime
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from datetime import datetime, timedelta
from collections import defaultdict


class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)

    def __call__(self, request):
        # Get the user information
        user = "Anonymous"
        if hasattr(request, 'user') and request.user.is_authenticated:
            user = request.user.username

        # Log the request information
        log_message = f"{datetime.now()} - User: {user} - \
            Path: {request.path}\n"

        # Write to a log file
        with open('requests.log', 'a') as f:
            f.write(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)

    def __call__(self, request):
        # Get current hour
        current_hour = datetime.now().hour
        print(current_hour)

        # Check if the request is for messaging (adjust path as needed)
        # if request.path.startswith('/messaging/') \
        #     or request.path.startswith('/chat/'):
        # Restrict access between 9 PM (21) and 6 AM (6)
        if current_hour >= 21 or current_hour < 6:
            return HttpResponseForbidden(
                "Messaging is only available between 6 AM and 9 PM.",
            )

        return self.get_response(request)


class OffensiveLanguageMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        # Store IP addresses and their request timestamps
        self.ip_tracker = defaultdict(list)
        self.limit = 1  # 5 messages
        self.time_window = 60  # 60 seconds (1 minute)

    def __call__(self, request):
        ip_address = self.get_client_ip(request)

        # Only check POST requests to messaging endpoints
        if request.method == 'POST':
            current_time = datetime.now()

            # Clean up old requests for this IP
            self.cleanup_old_requests(ip_address, current_time)

            # Check if limit exceeded
            if len(self.ip_tracker[ip_address]) >= self.limit:
                return HttpResponseForbidden(
                    "Rate limit exceeded: Maximum 5 messages per minute. "
                    "Please try again later."
                )

            # Record this request
            self.ip_tracker[ip_address].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def cleanup_old_requests(self, ip_address, current_time):
        # Remove timestamps older than our time window
        cutoff = current_time - timedelta(seconds=self.time_window)
        self.ip_tracker[ip_address] = [
            t for t in self.ip_tracker[ip_address]
            if t > cutoff
        ]


class RolepermissionMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        # Define protected paths (adjust as needed)
        self.admin_paths = ['/admin-actions/', '/manage-content/']
        self.moderator_paths = ['/moderate/']

    def __call__(self, request):
        # Check if path requires special permissions
        path = request.path

        # Skip permission check for non-protected paths
        if not any(path.startswith(p) for p in self.admin_paths +
                   self.moderator_paths):
            return self.get_response(request)

        # Check authentication
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Authentication required")

        # Check admin permissions for admin paths
        if any(path.startswith(p) for p in self.admin_paths):
            if not (request.user.is_superuser or request.user.is_staff):
                return HttpResponseForbidden("Admin privileges required")

        # Check moderator permissions for moderator paths
        if any(path.startswith(p) for p in self.moderator_paths):
            if not hasattr(request.user, 'is_moderator') or not \
                    request.user.is_moderator:
                return HttpResponseForbidden("Moderator privileges required")

        return self.get_response(request)
