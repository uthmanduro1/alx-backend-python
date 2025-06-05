import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    