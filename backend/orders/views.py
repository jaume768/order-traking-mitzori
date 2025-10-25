from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderHistory
from .serializers import OrderSerializer, OrderTrackingSerializer


@method_decorator(csrf_exempt, name='dispatch')
class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for querying orders.
    Public endpoint for users to track their orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'order_number'
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'], url_path='track/(?P<order_number>[^/.]+)')
    def track(self, request, order_number=None):
        """
        Endpoint to track an order by its number.
        GET /api/orders/track/{order_number}/
        """
        try:
            order = get_object_or_404(Order, order_number=order_number)
            serializer = OrderTrackingSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def search(self, request):
        """
        Endpoint to search for an order.
        POST /api/orders/search/
        Body: {"order_number": "ABC123"}
        """
        order_number = request.data.get('order_number', '').strip()
        
        if not order_number:
            return Response(
                {'error': 'Order number is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            order = Order.objects.get(order_number=order_number)
            serializer = OrderTrackingSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Order not found. Please verify your order number.'},
                status=status.HTTP_404_NOT_FOUND
            )
