from common.base_consumer import BaseConsumer, States, AuthenticateSz
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model




class EchoConsumer(BaseConsumer):
    channel_layer_alias = settings.CHAT_CHANNEL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valid_cmds[States.authenticated] = [
            # cmds supported when authenticated
            ""
        ]

    def authenticate(self, data):
        sz = AuthenticateSz(data=data)
        if sz.is_valid(raise_exception=False):
            ...
        else:
            ...
