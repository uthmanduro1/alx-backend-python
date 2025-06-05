import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    class Meta:
        model = Message
        fields = {
            'sender__username': ['icontains', 'exact'],
            'conversation': ['exact'],
            'sent_at': ['gte', 'lte'],
        }