from rest_framework import status
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from typing import Any, TypedDict
from uuid import uuid4
from rest_framework import serializers

class RequestStructure(TypedDict):
    _req: str
    data: dict[Any, Any]
    cmd: str
    status: int

class ReceiveStructure(TypedDict):
    _req: str
    data: dict[Any, Any]
    cmd: str

class States:
    anonymous = "anonymous"
    authenticated = "authenticated"

class AuthenticateSz(serializers.Serializer):
    token = serializers.CharField()

class BaseConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valid_cmds = {
            States.anonymous: [],
            States.authenticated: [], # to be designed in sub class
        }
        self.state = States.anonymous

    async def send_json(self, data):
        txt_data:str = json.dumps(data)
        await self.send(text_data=txt_data)

    async def response(self, cmd:str, data: dict[Any, Any], status=status.HTTP_200_OK):
        req_data: RequestStructure = {
            "_req": data.get("_req") or str(uuid4().hex),
            "data": data,
            "cmd": cmd,
            "status": status,
        }
        await self.send_json(req_data)


    async def authenticate(self, data:dict[Any, Any]):
        # to be implemented in the sub class
        ...

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        # Remove from the group
        ...
        # await self.channel_layer.group_discard(
        #     self.user_group_name,
        #     self.channel_name
        # )

    async def receive(self, text_data=None, bytes_data=None):
        data: ReceiveStructure = json.loads(text_data)
        cmd: str = data['cmd']

        if cmd not in self.valid_cmds[self.state]:
            # when data cmd is not in valid_cmd current state
            await self.response(cmd=cmd, data={"messages": [f"CMD '{cmd}' not supported"]}, status=status.HTTP_404_NOT_FOUND)
        else:
            handler = getattr(self, f"{cmd}", None)
            if not handler:
                await self.response(cmd=cmd, data={"messages": [f"CMD '{cmd}' not supported"], "_req": data["_req"]}, status=status.HTTP_404_NOT_FOUND)
                return
            # found valid handler
            await handler(data=data["data"])
