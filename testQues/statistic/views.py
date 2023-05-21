from django.db.models import Count
from rest_framework.response import Response
from rest_framework.views import APIView

from notification_service.models import Mailing, Message
from notification_service.serializers import NotificationSerializer, MessageSerializer, NotificationSerializerSmall


# Create your views here.

class StatMailId(APIView):
    def get(self, request, id):

        mail = Mailing.objects.get(id=id)
        mailSerializer = NotificationSerializer(mail, many=False)

        message = Message.objects.filter(mailing=mail.id)
        messageSerializer = MessageSerializer(message, many=True)

        data = {
            "mail": mailSerializer.data,
            "message": messageSerializer.data
        }

        return Response(data)

class StatMail(APIView):
    def get(self, request):
        mail = Mailing.objects.all()

        data = []
        for i in mail:
            data.append(
                {
                    "mail": NotificationSerializerSmall(i, many=False).data,
                    "status": Message.objects.filter(mailing_id=i.id).values("status").annotate(statCount=Count("status")).values("status", "statCount")
                }
            )
        return Response(data)