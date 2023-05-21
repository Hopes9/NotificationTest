import datetime
from datetime import timedelta
from random import choice
import requests
import json
from faker import Faker

from .models import Mobile_operator_code, Mailing, Client, Message


def createFlushData():
    fake = Faker()

    for _ in range(10):
        code = fake.random_int(min=1000000000, max=9999999999)
        Mobile_operator_code.objects.create(code=code)

    for _ in range(20):
        status = choice(['Create', 'Waiting', 'Send', 'Error'])
        start_datetime = fake.date_time_this_decade()
        end_datetime = start_datetime + timedelta(hours=2)
        message_text = fake.text()
        code = choice(Mobile_operator_code.objects.all())
        tag = fake.word()
        Mailing.objects.create(status=status, start_datetime=start_datetime,
                               end_datetime=end_datetime, message_text=message_text,
                               code=code, tag=tag)

    for _ in range(30):
        phone_number = fake.random_int(min=10000000000, max=99999999999)
        mobile_operator_code = choice(Mobile_operator_code.objects.all())
        tag = fake.word()
        timezone = fake.random_int(min=-12, max=12)
        Client.objects.create(phone_number=phone_number, mobile_operator_code=mobile_operator_code,
                              tag=tag, timezone=timezone)

    mailings = Mailing.objects.all()
    clients = Client.objects.all()

    for _ in range(50):
        status = choice(['Send', 'Waiting', 'Error'])
        mailing = choice(mailings)
        client = choice(clients)
        Message.objects.create(status=status, mailing=mailing, client=client)


def SendMessageEveryDay():
    # TODO Send email every day
    print("send email")

def ActivateUsers(row):
    # TODO get list email list and status email
    filters = row.get("data")
    mailing = row.get("mailing")

    tag = filters.get("tag")
    code = filters.get("code")

    clients = Client.objects.all()
    if tag:
        clients = clients.filter(tag=tag)
    if code:
        clients = clients.filter(mobile_operator_code__client__id=code)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTU5NTM0NTEsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9ob3BlczkxNiJ9.C_kLzV9VilPn8tCyyoykf73u2H_WsiFKkZ2GWCZubEY'
    }
    listUserErrors = []
    for i in clients:
        print(i)
        mess = Message.objects.create(
            status="Waiting",
            mailing_id=mailing,
            client_id=i.id
        )
        url = f"https://probe.fbrq.cloud/v1/send/{i.id}"
        payload = json.dumps({
            "id": i.id,
            "phone": i.phone_number,
            "text": "Text"
        })
        try:
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.ok:
                mess.status = "Send"
                mess.save()
            else:
                mess.status = "Error"
                mess.error = response.text
                listUserErrors.append((i.id, mailing))

        except Exception as e:
            mess.status = "Error"
            mess.error = str(e)
            mess.save()
            listUserErrors.append((i.id, mailing))
