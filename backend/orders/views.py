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
    ViewSet para consultar pedidos.
    Endpoint público para que los usuarios rastreen sus pedidos.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'order_number'
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'], url_path='track/(?P<order_number>[^/.]+)')
    def track(self, request, order_number=None):
        """
        Endpoint para rastrear un pedido por su número.
        GET /api/orders/track/{order_number}/
        """
        try:
            order = get_object_or_404(Order, order_number=order_number)
            serializer = OrderTrackingSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Pedido no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['post'])
    def search(self, request):
        """
        Endpoint para buscar un pedido.
        POST /api/orders/search/
        Body: {"order_number": "ABC123"}
        """
        order_number = request.data.get('order_number', '').strip()
        
        if not order_number:
            return Response(
                {'error': 'Número de pedido requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            order = Order.objects.get(order_number=order_number)
            serializer = OrderTrackingSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(
                {'error': 'Pedido no encontrado. Verifica el número de pedido.'},
                status=status.HTTP_404_NOT_FOUND
            )
