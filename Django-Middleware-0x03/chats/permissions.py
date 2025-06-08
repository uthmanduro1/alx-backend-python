from rest_framework import permissions
from .models import Conversation


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission that allow only participant in a conversation to have access to it
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD","OPTIONS", "PUT", "PATCH", "DELETE"]:
            return request.user in obj.participants.all()
        return False     
