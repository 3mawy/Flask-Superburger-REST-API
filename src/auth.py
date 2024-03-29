import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN', 'superburger.us.auth0.com')
ALGORITHMS = ['RS256']
API_AUDIENCE = os.getenv('API_AUDIENCE', 'superapi')

# AuthError Exception


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        abort(401)

    parts = auth.split()

    if parts[0].lower() != "bearer":
        abort(401)

    elif len(parts) == 1:
        abort(401)

    elif len(parts) > 2:
        abort(401)

    token = parts[1]
    return token


def check_permissions(permission, payload):
    if "permissions" in payload:
        if permission in payload['permissions']:
            return True
    abort(401)


def verify_decode_jwt(token):
    jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/"
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                             "description": "token is expired"}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                             "description":
                                 "incorrect claims,"
                                 "please check the audience and issuer"}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header",
                             "description":
                                 "Unable to parse authentication"
                                 " token."}, 401)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
