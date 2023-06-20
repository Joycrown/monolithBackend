from django.contrib import admin

from .models import Admin, Message, MessageAttachment, GenericFileUpload


admin.site.register(Admin)
admin.site.register(Message)
admin.site.register(MessageAttachment)
admin.site.register(GenericFileUpload)
