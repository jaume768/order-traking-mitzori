from django.db import models
from django.utils import timezone


class Order(models.Model):
    """Modelo para gestionar pedidos y su seguimiento"""
    
    STATUS_CHOICES = [
        ('PENDING', 'Order Received'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('IN_TRANSIT', 'In Transit'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    # Información del pedido
    order_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Número de Pedido',
        help_text='Número único de pedido que el cliente usará para rastrear'
    )
    customer_name = models.CharField(
        max_length=200,
        verbose_name='Nombre del Cliente'
    )
    customer_email = models.EmailField(
        verbose_name='Email del Cliente',
        blank=True,
        null=True
    )
    customer_phone = models.CharField(
        max_length=20,
        verbose_name='Teléfono del Cliente',
        blank=True,
        null=True
    )
    
    # Dirección de entrega
    delivery_address = models.TextField(
        verbose_name='Dirección de Entrega'
    )
    delivery_city = models.CharField(
        max_length=100,
        verbose_name='Ciudad'
    )
    delivery_postal_code = models.CharField(
        max_length=10,
        verbose_name='Código Postal'
    )
    
    # Estado del pedido
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING',
        verbose_name='Estado'
    )
    current_location = models.CharField(
        max_length=200,
        verbose_name='Ubicación Actual',
        blank=True,
        null=True,
        help_text='Ubicación actual del pedido en el proceso de entrega'
    )
    
    # Fechas
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización'
    )
    estimated_delivery = models.DateTimeField(
        verbose_name='Fecha Estimada de Entrega',
        blank=True,
        null=True
    )
    delivered_at = models.DateTimeField(
        verbose_name='Fecha de Entrega',
        blank=True,
        null=True
    )
    
    # Notas adicionales
    notes = models.TextField(
        verbose_name='Notas',
        blank=True,
        null=True,
        help_text='Notas adicionales sobre el pedido'
    )
    
    # Retraso
    is_delayed = models.BooleanField(
        default=False,
        verbose_name='Pedido con Retraso',
        help_text='Marcar si el pedido va con retraso en la entrega'
    )
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Pedido {self.order_number} - {self.get_status_display()}"
    
    def get_progress_percentage(self):
        """Calcula el porcentaje de progreso basado en el estado"""
        progress_map = {
            'PENDING': 0,
            'PROCESSING': 20,
            'SHIPPED': 40,
            'IN_TRANSIT': 60,
            'OUT_FOR_DELIVERY': 80,
            'DELIVERED': 100,
            'CANCELLED': 0,
        }
        return progress_map.get(self.status, 0)


class OrderHistory(models.Model):
    """Historial de cambios de estado del pedido"""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name='Pedido'
    )
    status = models.CharField(
        max_length=20,
        choices=Order.STATUS_CHOICES,
        verbose_name='Estado'
    )
    location = models.CharField(
        max_length=200,
        verbose_name='Ubicación',
        blank=True,
        null=True
    )
    description = models.TextField(
        verbose_name='Descripción',
        blank=True,
        null=True
    )
    timestamp = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha y Hora'
    )
    
    class Meta:
        verbose_name = 'Historial de Pedido'
        verbose_name_plural = 'Historial de Pedidos'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.order.order_number} - {self.get_status_display()} - {self.timestamp}"
