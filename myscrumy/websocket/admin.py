from django.contrib import admin

# Register your models here.
from .models import ChatMessage, ConnectionModel

admin.site.register(ChatMessage)
admin.site.register(ConnectionModel)