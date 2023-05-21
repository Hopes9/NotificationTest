from django.utils import timezone
from datetime import timedelta, datetime

from django.utils import timezone
from django_q.models import Schedule
from django_q.tasks import async_chain, async_task, schedule
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Mailing
from .serializers import NotificationSerializer


def complete_chain(group_id, schedule_type, repeats, next_run):
    print(group_id, schedule_type, repeats, next_run)
    print("Complete")


class Notification(APIView):
    @staticmethod
    def get(request, *args, **kwargs):
        return Response(Mailing.objects.all().values())


    @staticmethod
    @swagger_auto_schema(responses={200: NotificationSerializer(many=True)})
    def post(request, *args, **kwargs):
        serializer = NotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        print(data)
        datetime_end = datetime.strptime(data.get("end_datetime"), '%Y-%m-%dT%H:%M:%S%z')

        if data.get("start_datetime"):
            datetime_start = datetime.strptime(data.get("start_datetime"), '%Y-%m-%dT%H:%M:%S%z')
            if datetime_start < timezone.now():
                datetime_start = timezone.now()
        else:
            datetime_start = timezone.now()
        if datetime_start < datetime_end:
            mailing = Mailing.objects.create(status="Waiting",
                                                     start_datetime=datetime_start,
                                                     end_datetime=data.get("end_datetime"),
                                                     message_text=data.get("message_text"),
                                                     code=data.get("code"),
                                                     tag=data.get("tag"))
            chain = [('notification_service.func.ActivateUsers', ({"mailing": mailing.id, "data": data},), {}), ]
            schedule(chain[0][0], *chain[0][1], **chain[0][2],
                                 schedule_type=Schedule.DAILY,
                                 name=str(mailing.id),
                                 repeats=(datetime_end - datetime_start).days,
                                 next_run=datetime_start + timezone.timedelta(days=1))
            serializer = NotificationSerializer(mailing)
            return Response(serializer.data)
        elif datetime_end > datetime_start:
            return Response({"Error": "Get end_datetime > datetime.now()"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Error": "Get current start_datetime and end_datetime"}, status=status.HTTP_400_BAD_REQUEST)

class NotificationEdit(RetrieveUpdateDestroyAPIView):
    queryset = Mailing.objects.all()
    serializer_class = NotificationSerializer