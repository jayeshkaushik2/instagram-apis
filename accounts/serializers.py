from rest_framework import serializers, exceptions
from . import messages as msg
from django.contrib.auth import get_user_model
from .models import FollowUps


User = get_user_model()


class ValidateLoginForm(serializers.Serializer):
    email = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    mobile = serializers.CharField(required=False)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        if (
            attrs.get("email") is None
            and attrs.get("username") is None
            and attrs.get("mobile") is None
        ):
            raise exceptions.ValidationError(
                {"errors": [msg.PHONE_NUMBER_EMAIL_OR_USERNAME_REQUIRED]}
            )
        return super().validate(attrs)


class ValidateRegisterForm(serializers.Serializer):
    email = serializers.CharField(required=True)
    mobile = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise exceptions.ValidationError({"errors": [msg.PASSWORDS_DOES_NOT_MATCH]})
        return super().validate(attrs)


class UserSz(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "username",
            "email",
            "mobile",
            "is_active",
            "profile_image",
            "followers",
            "following",
        )

    def get_followers(self, obj):
        res = FollowUps.objects.filter(following=obj).count()
        return res

    def get_following(self, obj):
        res = FollowUps.objects.filter(follower=obj).count()
        return res
