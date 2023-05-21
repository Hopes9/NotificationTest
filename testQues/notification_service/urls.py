from django.urls import path

from notification_service.views import Notification, NotificationEdit

urlpatterns = [
    path("", Notification.as_view()),
    path("<int:pk>", NotificationEdit.as_view()),
]
