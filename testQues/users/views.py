from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from notification_service.models import Client
from users.serializers import ClientSerializer


# Create your views here.

class Users(ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer



class UsersEdit(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
