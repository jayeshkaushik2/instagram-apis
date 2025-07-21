from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .consumer import ChatConsumer

routes = DefaultRouter()

urlpatterns = [
]


urlpatterns += routes.urls

websocket_urlpatterns = [
    re_path(r"^chat/$", ChatConsumer.as_asgi(), name="chat"),
]