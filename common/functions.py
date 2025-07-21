import jwt
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from django.conf import settings
from jwt.exceptions import InvalidTokenError
from asgiref.sync import sync_to_async

@sync_to_async
def async_get_user_from_access_token(token: str):
    """
    Asynchronously decode a JWT access token and return the associated user.
    """
    try:
        # Validate token
        UntypedToken(token)

        # Decode manually to extract user_id
        decoded_data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )

        user_id = decoded_data.get("user_id")
        if not user_id:
            raise ValueError("user_id not found in token")

        User = get_user_model()
        return User.objects.get(id=user_id)

    except (InvalidToken, TokenError, InvalidTokenError) as e:
        raise ValueError(f"Invalid token: {str(e)}")
    except User.DoesNotExist:
        raise ValueError("User not found for given token")
