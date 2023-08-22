from rest_framework import serializers
from .models import Chamber, Chat, Bot


class ChamberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamber 
        fields = "__all__"
    

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat 
        fields = '__all__'
    

class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot 
        fields = '__all__'