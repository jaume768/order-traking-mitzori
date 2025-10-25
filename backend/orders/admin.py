from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderHistory


class OrderHistoryInline(admin.TabularInline):
    """Inline para mostrar el historial dentro del pedido"""
    model = OrderHistory
    extra = 1
    fields = ('status', 'location', 'description', 'timestamp')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin personalizado para gestionar pedidos"""
    
    list_display = (
        'order_number',
        'customer_name',
        'status_badge',
        'current_location',
        'progress_bar',
        'created_at',
        'estimated_delivery'
    )
    
    list_filter = (
        'status',
        'created_at',
        'delivery_city'
    )
    
    search_fields = (
        'order_number',
        'customer_name',
        'customer_email',
        'customer_phone',
        'delivery_address'
    )
    
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('order_number', 'status', 'current_location', 'is_delayed')
        }),
        ('Información del Cliente', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Dirección de Entrega', {
            'fields': ('delivery_address', 'delivery_city', 'delivery_postal_code')
        }),
        ('Fechas', {
            'fields': ('estimated_delivery', 'delivered_at')
        }),
        ('Notas', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    inlines = [OrderHistoryInline]
    
    def status_badge(self, obj):
        """Muestra el estado con un badge de color"""
        colors = {
            'PENDING': '#ffc107',
            'PROCESSING': '#17a2b8',
            'SHIPPED': '#007bff',
            'IN_TRANSIT': '#6610f2',
            'OUT_FOR_DELIVERY': '#fd7e14',
            'DELIVERED': '#28a745',
            'CANCELLED': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Estado'
    
    def progress_bar(self, obj):
        """Muestra una barra de progreso visual"""
        percentage = obj.get_progress_percentage()
        color = '#28a745' if percentage == 100 else '#007bff'
        return format_html(
            '<div style="width: 100px; background-color: #e9ecef; border-radius: 3px;">'
            '<div style="width: {}%; background-color: {}; height: 20px; '
            'border-radius: 3px; text-align: center; color: white; font-size: 11px; '
            'line-height: 20px;">{} %</div></div>',
            percentage,
            color,
            percentage
        )
    progress_bar.short_description = 'Progreso'
    
    def save_model(self, request, obj, form, change):
        """Guarda el modelo y crea una entrada en el historial"""
        is_new = obj.pk is None
        old_status = None
        
        if change and not is_new:
            old_obj = Order.objects.get(pk=obj.pk)
            old_status = old_obj.status
        
        super().save_model(request, obj, form, change)
        
        # Crear entrada en el historial si el estado cambió
        if is_new or (old_status and old_status != obj.status):
            OrderHistory.objects.create(
                order=obj,
                status=obj.status,
                location=obj.current_location or '',
                description=f'Estado actualizado a {obj.get_status_display()}'
            )


@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    """Admin para el historial de pedidos"""
    
    list_display = (
        'order',
        'status',
        'location',
        'timestamp'
    )
    
    list_filter = (
        'status',
        'timestamp'
    )
    
    search_fields = (
        'order__order_number',
        'location',
        'description'
    )
    
    readonly_fields = ('timestamp',)
    
    date_hierarchy = 'timestamp'


# Personalizar el admin site
admin.site.site_header = 'Sistema de Seguimiento de Pedidos - Mitzori'
admin.site.site_title = 'Admin Pedidos'
admin.site.index_title = 'Gestión de Pedidos'
