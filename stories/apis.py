from django.shortcuts import render
from rest_framework import viewsets, response, permissions
from .models import Stories
from .serializers import StoriesSz
from django_filters import rest_framework as filters

# Create your views here.
"""
need to have permissions
"""


class StoriesFilter(filters.FilterSet):
    class Meta:
        model = Stories
        fields = {
            "name": ["exact", "icontains"],
            "user": ["exact"],
            "viewers": ["exact"],
        }


class StoriesViewSet(viewsets.ModelViewSet):
    serializer_class = StoriesSz

    search_fields = ["user", "viewers"]
    ordering_fields = ["user", "viewers"]
    filterset_class = StoriesFilter

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Stories.objects.all()
