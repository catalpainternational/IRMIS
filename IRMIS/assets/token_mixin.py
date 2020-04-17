import jwt
from django.http.response import JsonResponse
from django.conf import settings


def get_jwt_token_from_request(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    auth_header_prefix = "Bearer"

    if not auth_header:
        raise jwt.InvalidTokenError("The Authorization header must not be empty.")
    if not auth_header.startswith(auth_header_prefix):
        raise jwt.InvalidTokenError(
            'The Authorization header must start with "{}".'.format(auth_header_prefix)
        )

    return auth_header[len(auth_header_prefix) + 1 :]


class JWTRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            token = get_jwt_token_from_request(request)
            if len(token) >= 1:
                jwt.decode(
                    token,
                    settings.JWT_AUTH["JWT_SECRET_KEY"],
                    algorithms=[settings.JWT_AUTH["JWT_ALGORITHM"]],
                )
        except jwt.InvalidTokenError as e:
            return JsonResponse({"error": "Unauthorized Error: %s" % e}, status=401)
        return super(JWTRequiredMixin, self).dispatch(request, *args, **kwargs)
