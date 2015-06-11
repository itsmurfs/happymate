from rest_framework import serializers
from happyfridge.models import Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model= Item
        fields = ['id','name', 'status', 'quantity']
