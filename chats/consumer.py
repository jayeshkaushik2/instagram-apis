from common.base_consumer import BaseConsumer, States, AuthenticateSz
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, SlidingToken
from django.contrib.auth import get_user_model
from enum import Enum
from rest_framework import status, serializers
from typing import Any
from accounts.models import User
from chats import messages as chat_msgs

class SupportedCmds(Enum):
    authenticate = "authenticate"
    # Add other commands as needed
    send_message = "send_message"
    message_sent = "message_sent"
    message_received = "message_received"
    message_seen = "message_seen"

class SendMessageValidator(serializers.Serializer):
    message = serializers.CharField(required=True)
    send_to = serializers.IntegerField(required=True)
    send_time = serializers.DateTimeField(required=True)
    message_request = serializers.BooleanField(required=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(pk=attrs["send_to"])
            if not user.is_active:
                raise serializers.ValidationError({"errors": ["User doesn't have an active account."]})
            # TODO have to add validation for message_request and does the receiver even follow the sender
        except User.DoesNotExist:
            raise serializers.ValidationError({"errors": ["User is not registered."]})
        return super().validate(attrs)


class ChatConsumer(BaseConsumer):
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
    
    async def get_user_room(self, user_id: int) -> str:
        return f"user_{user_id}"

    async def add_user_to_channel(self, user: Any) -> None:
        room_name = await self.get_user_room(user.id)
        await self.channel_layer.group_add(room_name, self.channel_name)

    async def authenticate(self, data, **kwargs):
        sz = AuthenticateSz(data=data)
        if sz.is_valid(raise_exception=False):
            try:
                user_id = SlidingToken(token=sz.validated_data['token']).user_id
                user = await get_user_model().objects.aget(id=user_id)
                self.state = States.authenticated
                self.scopes["user"] = user
                # add user to channel
                await self.add_user_to_channel(user=user)
                # accept the connect request
                await self.connect()
                await self.response(
                    cmd=SupportedCmds.authenticate.value,
                    data={"messages": ["Authentication successful"]},
                    status=status.HTTP_200_OK,
                )
            except Exception:
                await self.response(
                    cmd=SupportedCmds.authenticate.value,
                    data={"messages": ["Invalid token"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            print(f"cmd: authenticate error {sz.errors}")
            await self.response(
                cmd=SupportedCmds.authenticate.value,
                data={"messages": [chat_msgs.INVALID_MESSAGE_PAYLOAD]},
                status=status.HTTP_400_BAD_REQUEST,
                )

    async def send_message(self, data, **kwargs):
        # Implementation for sending a message
        print(f"cmd: send_message received {data}")
        sz = SendMessageValidator(data=data)
        if sz.is_valid(raise_exception=False):
            data: dict[str, Any] = sz.validated_data
            recipient: User = await User.objects.aget(pk=data["send_to"])
            recipient_room_name: str = await self.get_user_room(recipient.id)

            await self.channel_layer.group_send(
                recipient_room_name,
                {
                    "type": "event.message_received",
                    "cmd": SupportedCmds.send_message.value,
                    "data": {
                        "message": data["message"],
                        "sender_id": recipient.id,
                        "sender_username": recipient.username,
                    }
                }
            )

        else:
            await self.response(
                cmd=SupportedCmds.send_message.value,
                data={"messages": [chat_msgs.INVALID_MESSAGE_PAYLOAD]},
                status=status.HTTP_400_BAD_REQUEST,
                )

    async def message_sent(self, data, **kwargs):
        # Implementation for handling message sent event
        print(f"cmd: message_sent received {data}")
        pass

    async def message_received(self, data, **kwargs):
        # Implementation for handling message received event
        print(f"cmd: message_received received {data}")
        pass

    async def message_seen(self, data, **kwargs):
        # Implementation for handling message seen event
        print(f"cmd: message_seen received {data}")
        pass

    async def event_message_received(self, event: dict[str, Any]) -> None:
        print(f"event: message_received {event}")
        self.response(
            cmd=event["cmd"],
            data=event["data"],
        )