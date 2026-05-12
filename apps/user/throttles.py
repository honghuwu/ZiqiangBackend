from rest_framework.throttling import SimpleRateThrottle


class RegisterCodeRateThrottle(SimpleRateThrottle):
    """
    Rate throttle for registration code endpoints.
    - Authenticated users are throttled by user ID
    - Anonymous users are throttled by IP address
    """
    scope = 'register_code'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        if ident is None:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident,
        }


class LoginRateThrottle(SimpleRateThrottle):
    """
    Rate throttle for login endpoint to prevent brute force attacks.
    - Throttle by IP address for anonymous users
    - By default: 5 attempts per minute per IP
    """
    scope = 'login'

    def get_cache_key(self, request, view):
        # Throttle by IP address
        ident = self.get_ident(request)
        
        if ident is None:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident,
        }