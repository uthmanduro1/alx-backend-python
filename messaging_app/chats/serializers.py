from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()  # For nested representation

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_name', 'conversation', 'message_body', 'sent_at']

    def get_sender_name(self, obj):
        return obj.sender.username  # shows sender's username instead of just UUID  

    def validate_message_body(self, value):
        if not value or len(value.strip()) < 1:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',   # UUID
            'participants',      # ManyToMany (User)
            'created_at',        # Timestamp
            'messages',          # Nested messages
        ]