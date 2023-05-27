from rest_framework import serializers
from .models import Stories


class StoriesSz(serializers.ModelSerializer):
    class Meta:
        model = Stories
        fields = (
            "id",
            "user",
            "video",
            "viewers",
        )
