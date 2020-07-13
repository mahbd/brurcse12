from django.contrib import admin
from .models import Keywords, Problems, Topic, Technique, Handle


admin.site.register(Handle)
admin.site.register(Keywords)
admin.site.register(Problems)
admin.site.register(Topic)
admin.site.register(Technique)
