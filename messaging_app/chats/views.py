from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']

    def get_queryset(self):
        conversation_id = self.request.query_params.get("conversation")
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id)
        return Message.objects.all()

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)