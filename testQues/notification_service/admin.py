from django.contrib import admin

from notification_service.models import Mailing, Message, Client, Mobile_operator_code


@admin.register(Mobile_operator_code)
class Mobile_operator_codeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'code'
    )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'status', 'error', 'mailing', 'client'
    )

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'phone_number', 'mobile_operator_code', 'tag', 'timezone'
    )

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'created_at', 'status', 'start_datetime', 'end_datetime', 'message_text', 'code', 'tag'
    )

