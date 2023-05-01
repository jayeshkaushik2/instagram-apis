from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from .apis import login, register, UserViewSet

routes = DefaultRouter()
routes.register("accounts", UserViewSet, basename="accounts")

urlpatterns = [
    path("login/", login, name="login"),
    path("register/", register, name="register"),
]


urlpatterns += routes.urls
