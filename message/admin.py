from django.contrib import admin
from .models import GroupInfo, Message, LastMessage

admin.site.register(GroupInfo)
admin.site.register(Message)
admin.site.register(LastMessage)
