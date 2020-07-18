from django.contrib import admin
from .models import Faq, UpdateTime, Announce, SecretKeys

admin.site.register(Faq)
admin.site.register(UpdateTime)
admin.site.register(Announce)
admin.site.register(SecretKeys)
