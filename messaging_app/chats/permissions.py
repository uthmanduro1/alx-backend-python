from rest_framework.permissions import BasePermission
from .models import Conversation


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission that allow only participant in a conversation to have access to it
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()
            