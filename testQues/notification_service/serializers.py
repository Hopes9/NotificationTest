from rest_framework import serializers

from notification_service.models import Mailing, Message


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = "__all__"

class NotificationSerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ["id", "status", "start_datetime", "end_datetime", ]

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"