from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import generics


class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all().select_related("profile")
        return queryset


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all().select_related("profile")
    serializer_class = UserSerializer
