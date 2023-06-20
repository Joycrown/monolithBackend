from rest_framework.fields import CurrentUserDefault
from rest_framework import serializers

from admin.models import (
    Admin, GenericFileUpload, Message, MessageAttachment
)


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admin
        fields = '__all__'


class GenericFileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenericFileUpload
        fields = "__all__"


class MessageAttachmentSerializer(serializers.ModelSerializer):
    attachment = GenericFileUploadSerializer()

    class Meta:
        model = MessageAttachment
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField("get_sender_data")
    sender_id = serializers.CharField(write_only=True)
    receiver = serializers.SerializerMethodField("get_receiver_data")
    receiver_id = serializers.CharField(write_only=True)
    message_attachments = MessageAttachmentSerializer(
        read_only=True, many=True)

    class Meta:
        model = Message
        fields = "__all__"

    def get_receiver_data(self, obj):
        from core.api.serializers import ListUserSerializer
        return ListUserSerializer(obj.receiver).data

    def get_sender_data(self, obj):
        from core.api.serializers import ListUserSerializer
        return ListUserSerializer(obj.sender).data
