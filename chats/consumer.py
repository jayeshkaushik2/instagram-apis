from common.base_consumer import BaseConsumer, States, AuthenticateSz
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, SlidingToken
from django.contrib.auth import get_user_model
from enum import Enum
from rest_framework import status

class SupportedCmds(Enum):
    authenticate = "authenticate"
    # Add other commands as needed
    send_message = "send_message"
    message_sent = "message_sent"
    message_received = "message_received"
    message_seen = "message_seen"

class EchoConsumer(BaseConsumer):
    channel_layer_alias = settings.CHAT_CHANNEL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Define commands supported when anonymous
        self.valid_cmds[States.anonymous] = [
            SupportedCmds.authenticate.value,
        ]
        # Define commands supported when authenticated
        self.valid_cmds[States.authenticated] = [
            SupportedCmds.send_message.value,
        ]

    async def authenticate(self, data, **kwargs):
        sz = AuthenticateSz(data=data)
        if sz.is_valid(raise_exception=False):
            try:
                user_id = SlidingToken(token=sz.validated_data['token']).user_id
                user = get_user_model().objects.get(id=user_id)
                self.state = States.authenticated
                self.user = user
                self.channel_layer_alias = f"{settings.CHAT_CHANNEL}_{user.id}"
                self.response(
                    cmd=SupportedCmds.authenticate.value,
                    data={"messages": ["Authentication successful"]},
                    status=status.HTTP_200_OK,
                )
            except Exception:
                self.response(
                    cmd=SupportedCmds.authenticate.value,
                    data={"messages": ["Invalid token"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return self.response(
                cmd=SupportedCmds.authenticate.value,
                data=sz.errors, 
                status=status.HTTP_400_BAD_REQUEST,
                )
