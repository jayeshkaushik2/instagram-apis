import asyncio
import websockets
import json
import time

WS_URL = "ws://localhost:8080/chat/"

# Example tokens
TOKEN1 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU1NzEyMjgyLCJpYXQiOjE3NTMxMjAyODIsImp0aSI6IjI5ZGRkZjM3YjU1ZjRlMjc4YzdjYmI2MTBjZjg3NDQ4IiwidXNlcl9pZCI6MX0.oU-JfXXIwQe7Dv2cqh4o5K7XVMw6SB4yCZ22LgBHKyU"
TOKEN2 = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU1NzEyMzI4LCJpYXQiOjE3NTMxMjAzMjgsImp0aSI6Ijk0NmEwNDUwMDNhMTRhNGI5NjI1NzljM2ZiMzM1MWE4IiwidXNlcl9pZCI6Mn0.ZlO6eO7OiG5sffT8prU8HQiDO3ZFM-R_CeQ24VRzDM0"

async def authenticate(ws, token, label):
    auth_payload = {
        "cmd": "authenticate",
        "data": {"token": token},
        "_req": f"{label}_auth"
    }
    await ws.send(json.dumps(auth_payload))
    response = await ws.recv()
    print(f"[{label}] Auth Response: {response}")


async def user1_send_message(ws1):
    message_payload = {
        "cmd": "send_message",
        "data": {
            "message": "Hello from token1!",
            "send_to": 2,  # Replace with actual user ID
            "send_time": time.time(),
            "message_request": True,
        },
        "_req": "token1_send"
    }
    await asyncio.sleep(2)  # Give token2 time to connect and authenticate
    await ws1.send(json.dumps(message_payload))
    print("[token1] Sent message")


async def run():
    async with websockets.connect(WS_URL) as ws1, websockets.connect(WS_URL) as ws2:
        await asyncio.gather(
            authenticate(ws1, TOKEN1, "token1"),
            authenticate(ws2, TOKEN2, "token2"),
        )
        await user1_send_message(ws1)

        # Optionally keep receiving messages
        async def listen(ws, label):
            try:
                async for message in ws:
                    print(f"[{label}] Received: {message}")
            except websockets.ConnectionClosed:
                print(f"[{label}] Connection closed")

        await asyncio.gather(
            listen(ws1, "token1"),
            listen(ws2, "token2"),
        )

if __name__ == "__main__":
    asyncio.run(run())
