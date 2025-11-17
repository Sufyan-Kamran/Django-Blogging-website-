from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class JWTRefreshMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get("access_token")

        if not access_token:
            return None

        try:
            AccessToken(access_token)
            return None
        except Exception:
            refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                return None

            try:
                refresh = RefreshToken(refresh_token)
                new_access = str(refresh.access_token)

                request.META["HTTP_AUTHORIZATION"] = f"Bearer {new_access}"

                request.new_access_token = new_access

            except Exception:
                return JsonResponse({"detail": "Session expired"}, status=401)

    def process_response(self, request, response):
        new_access = getattr(request, "new_access_token", None)

        if new_access:
            response.set_cookie(
                "access_token",
                new_access,
                httponly=True,
                secure=False,
                samesite="Lax",
            )

        return response
