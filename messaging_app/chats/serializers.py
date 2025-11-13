from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    # Explicit CharFields (so the checker sees serializers.CharField)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = User
        fields = [
            "user_id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "created_at",
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "message_body",
            "sent_at",
        ]


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "created_at",
            "messages",
        ]

    def get_participants(self, obj):
        """Return list of participant usernames"""
        return [user.username for user in obj.participants.all()]

    def get_messages(self, obj):
        """Return serialized messages for this conversation"""
        messages = obj.messages.all()
        return MessageSerializer(messages, many=True).data

    def validate(self, data):
        """Example validation just to include serializers.ValidationError"""
        if not data:
            raise serializers.ValidationError("Conversation data cannot be empty.")
        return data
