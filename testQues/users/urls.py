from django.urls import path

from users.views import Users, UsersEdit

urlpatterns = [
    path("", Users.as_view()),
    path("<int:pk>", UsersEdit.as_view()),
]
