from django.urls import path

from statistic.views import StatMail, StatMailId

urlpatterns = [
    path("mailing/<int:id>", StatMailId.as_view()),
    path("mailing/", StatMail.as_view()),
    # path("<int:pk>", UsersEdit.as_view()),

]
