from rest_framework import serializers
from .models import Order, OrderHistory


class OrderHistorySerializer(serializers.ModelSerializer):
    """Serializer para el historial de pedidos"""
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = OrderHistory
        fields = [
            'id',
            'status',
            'status_display',
            'location',
            'description',
            'timestamp'
        ]


class OrderSerializer(serializers.ModelSerializer):
    """Serializer para pedidos"""
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    progress_percentage = serializers.IntegerField(source='get_progress_percentage', read_only=True)
    history = OrderHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'customer_name',
            'customer_email',
            'customer_phone',
            'delivery_address',
            'delivery_city',
            'delivery_postal_code',
            'status',
            'status_display',
            'current_location',
            'progress_percentage',
            'created_at',
            'updated_at',
            'estimated_delivery',
            'delivered_at',
            'notes',
            'history'
        ]
        read_only_fields = ['created_at', 'updated_at']


class OrderTrackingSerializer(serializers.ModelSerializer):
    """Serializer simplificado para el tracking público (sin datos sensibles)"""
    
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    progress_percentage = serializers.IntegerField(source='get_progress_percentage', read_only=True)
    history = OrderHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'order_number',
            'status',
            'status_display',
            'current_location',
            'progress_percentage',
            'estimated_delivery',
            'delivered_at',
            'is_delayed',
            'history'
        ]
