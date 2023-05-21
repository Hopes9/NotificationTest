from django.db import models
from django.utils import timezone
from django_q.models import Schedule, Task, Success


class Mobile_operator_code(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10)

class Mailing(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    CATEGORY_CHOICES = (
        ("Create", "Создано"),
        ("Waiting", "Ожидание отправки"),
        ("Send", "Отправка"),
        ("Error", "Ошибка")
    )
    status = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default="Create")
    start_datetime = models.DateTimeField(default=timezone.now)
    end_datetime = models.DateTimeField()
    message_text = models.TextField(blank=True)
    code = models.ForeignKey(Mobile_operator_code, on_delete=models.CASCADE, null=True, blank=True)
    tag = models.CharField(null=True, blank=True, max_length=255)

    def __str__(self):
        return str(self.id)

    def delete(self, *args, **kwargs):
        Schedule.objects.filter(name=str(self.id)).delete()
        Task.objects.filter(name=str(self.id)).delete()
        Message.objects.filter(mailing_id=self.id).delete()
        Success.objects.filter(name=str(self.id)).delete()
        super().delete(*args, **kwargs)

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=11, unique=True)
    mobile_operator_code = models.ForeignKey(Mobile_operator_code, on_delete=models.CASCADE)
    tag = models.CharField(max_length=255)
    timezone = models.IntegerField(blank=True)

    def __str__(self):
        return str(self.id)

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    created_datetime = models.DateTimeField(auto_now_add=True)

    CATEGORY_CHOICES = (
        ("Send", "Отправлено"),
        ("Waiting", "Ожидание"),
        ("Error", "Ошибка")
    )
    status = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    error = models.TextField(null=True, blank=True)
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
