from rest_framework import response, decorators, status, permissions
from .serializers import ValidateLoginForm, UserSz, ValidateRegisterForm
from django.db.models import Q
from . import messages as msg
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from django_filters import rest_framework as filters

from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.


@decorators.api_view(["POST"])
def login(request):
    sz = ValidateLoginForm(data=request.data)
    if sz.is_valid(raise_exception=True):
        mobile = sz.validated_data.get("mobile")
        email = sz.validated_data.get("email")
        username = sz.validated_data.get("username")
        password = sz.validated_data.get("password")

        user = User.objects.filter(
            Q(mobile=mobile) | Q(email=email) | Q(username=username)
        ).first()

        if user is None:
            return response.Response(
                {"errors": [msg.USER_NOT_FOUND]}, status=status.HTTP_404_NOT_FOUND
            )

        if user.check_password(password):
            sz = UserSz(instance=user, many=False)
            refresh = RefreshToken.for_user(user=user)
            data = sz.data
            data["tokens"] = {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
            return response.Response(data)
        else:
            return response.Response(
                {"errors": [msg.INCORRECT_PASSWORD]}, status=status.HTTP_400_BAD_REQUEST
            )
    return response.Response({"errors": [msg.INVALID_DATA]})


@decorators.api_view(["POST"])
def register(request):
    sz = ValidateRegisterForm(data=request.data)
    if sz.is_valid(raise_exception=True):
        mobile = sz.validated_data.get("mobile")
        email = sz.validated_data.get("email")
        username = sz.validated_data.get("username")
        password = sz.validated_data.get("password")

        if User.objects.filter(
            Q(mobile=mobile) | Q(email=email) | Q(username=username)
        ).exists():
            return response.Response(
                {"errors": [msg.USER_ALREADY_EXISTS]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sz.validated_data.pop("confirm_password")
        user = User.objects.create(**sz.validated_data)
        user.set_password(password)
        user.save()

        sz = UserSz(instance=user, many=False)
        refresh = RefreshToken.for_user(user=user)
        data = sz.data
        data["tokens"] = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
        return response.Response(data)
    return response.Response({"errors": [msg.INVALID_DATA]})


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            "name": ["exact", "icontains"],
            "username": ["exact", "icontains"],
            "email": ["exact", "icontains"],
            "mobile": ["exact", "icontains"],
            "date_joined": ["exact", "gt", "lt"],
            "last_login": ["exact", "gt", "lt"],
            "is_admin": ["exact"],
            "is_staff": ["exact"],
            "is_superuser": ["exact"],
        }


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSz

    search_fields = ["username", "email", "mobile", "name"]
    ordering_fields = ["username", "email", "mobile", "date_joined", "last_login"]
    filterset_class = UserFilter

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(is_active=True)
