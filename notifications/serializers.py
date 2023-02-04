from rest_framework import serializers
from .models import Notification
from core.api.serializers import ListUserSerializer
from block.api.serializers import PostSerializer,CommentSerializer

class NotificationSerializer(serializers.ModelSerializer):

    from_user = ListUserSerializer()
    to_user = ListUserSerializer()
    noti_count = serializers.SerializerMethodField(read_only=True)
    post = PostSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id','from_user','to_user','noti_count','post','comment','notification_type','comments','user_has_seen','created_time_ago']

    def get_noti_count(self,obj):
        count = self.context.get('noti_count')
        return count
