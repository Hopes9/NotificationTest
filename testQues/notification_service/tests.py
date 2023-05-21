from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .models import Mailing
from .serializers import NotificationSerializer


class NotificationTests(TestCase):
    def setUp(self):
        self.url = reverse('notification')

    def test_get_notification_returns_all_mailings(self):
        mailing1 = Mailing.objects.create(status="Waiting", message_text="Test message 1")
        mailing2 = Mailing.objects.create(status="Waiting", message_text="Test message 2")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = NotificationSerializer([mailing1, mailing2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_post_notification_creates_mailing_and_schedules_task(self):
        data = {
            "message_text": "Test message",
            "start_datetime": "2023-05-21T12:00:00+00:00",
            "end_datetime": "2023-05-22T12:00:00+00:00",
            "code": "test_code",
            "tag": "test_tag"
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        mailing = Mailing.objects.first()
        self.assertIsNotNone(mailing)
        self.assertEqual(mailing.status, "Waiting")
        self.assertEqual(mailing.message_text, "Test message")
        self.assertEqual(mailing.start_datetime.isoformat(), "2023-05-21T12:00:00+00:00")
        self.assertEqual(mailing.end_datetime.isoformat(), "2023-05-22T12:00:00+00:00")
        self.assertEqual(mailing.code, "test_code")
        self.assertEqual(mailing.tag, "test_tag")

        scheduled_task = mailing.schedules.first()
        self.assertIsNotNone(scheduled_task)
        self.assertEqual(scheduled_task.func, 'notification_service.func.ActivateUsers')
        self.assertEqual(scheduled_task.kwargs, {"mailing": mailing.id, "data": data})
        self.assertEqual(scheduled_task.schedule_type, 'D')
        self.assertEqual(scheduled_task.repeats, 1)
        self.assertEqual(scheduled_task.next_run, mailing.start_datetime + timezone.timedelta(days=1))

    def test_post_notification_with_invalid_data_returns_bad_request(self):
        data = {
            "message_text": "Test message",
            "start_datetime": "2023-05-22T12:00:00+00:00",
            "end_datetime": "2023-05-21T12:00:00+00:00",
            "code": "test_code",
            "tag": "test_tag"
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class NotificationEditTests(TestCase):
    def setUp(self):
        self.mailing = Mailing.objects.create(status="Waiting", message_text="Test message")
        self.url = reverse('notification-edit', kwargs={'pk': self.mailing.pk})

    def test_get_notification_edit_returns_mailing(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = NotificationSerializer(self.mailing).data
        self.assertEqual(response.data, expected_data)

    def test_update_notification_edit_updates_mailing(self):
        data = {
            "message_text": "Updated message",
            "start_datetime": "2023-05-22T12:00:00+00:00",
            "end_datetime": "2023-05-23T12:00:00+00:00",
            "code": "test_code",
            "tag": "test_tag"
        }

        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.mailing.refresh_from_db()
        self.assertEqual(self.mailing.message_text, "Updated message")
        self.assertEqual(self.mailing.start_datetime.isoformat(), "2023-05-22T12:00:00+00:00")
        self.assertEqual(self.mailing.end_datetime.isoformat(), "2023-05-23T12:00:00+00:00")
        self.assertEqual(self.mailing.code, "test_code")
        self.assertEqual(self.mailing.tag, "test_tag")

    def test_delete_notification_edit_deletes_mailing(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        exists = Mailing.objects.filter(pk=self.mailing.pk).exists()
        self.assertFalse(exists)
