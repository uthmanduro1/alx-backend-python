from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from rest_framework.response import Response
from .filters import MessageFilter
from .pagination import MessagePagination
from django_filters.rest_framework import DjangoFilterBackend


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
    filter_backends = [DjangoFilterBackend]
    filter_class = [MessageFilter]
    pagination_class = MessagePagination
    ordering_fields = ['sent_at']

    def get_queryset(self):
        conversation_id = self.request.query_params.get("conversation")
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id)
        return Message.objects.all()

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if self.request.user not in conversation.participant.all():
            return Response("You are not a participant of this Conversation", status.HTTP_403_FORBIDDEN)
        serializer.save(sender=self.request.user)