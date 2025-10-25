import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from orders.models import Order, OrderHistory


class Command(BaseCommand):
    help = 'Importa pedidos desde un CSV de Shopify'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Ruta al archivo CSV')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        
        self.stdout.write(self.style.SUCCESS(f'📦 Importando pedidos desde {csv_file}...'))
        
        # Diccionario para agrupar pedidos por número
        orders_dict = {}
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                order_id = row['Id']
                order_number = row['Name']  # #1002, #1003, etc.
                
                # Saltar si ya procesamos este pedido
                if order_number in orders_dict:
                    continue
                
                # Extraer datos relevantes
                shipping_name = row['Shipping Name'] or row['Billing Name']
                shipping_email = row['Email']
                shipping_phone = row['Shipping Phone'] or row['Billing Phone']
                
                # Construir dirección completa
                shipping_address = row['Shipping Address1'] or row['Billing Address1']
                shipping_address2 = row['Shipping Address2'] or row['Billing Address2']
                if shipping_address2:
                    shipping_address += f", {shipping_address2}"
                
                shipping_city = row['Shipping City'] or row['Billing City']
                shipping_zip = row['Shipping Zip'] or row['Billing Zip']
                shipping_province = row['Shipping Province'] or row['Billing Province']
                shipping_country = row['Shipping Country'] or row['Billing Country']
                
                # Dirección completa
                full_address = f"{shipping_address}, {shipping_city}"
                if shipping_province:
                    full_address += f", {shipping_province}"
                full_address += f", {shipping_country}"
                
                # Parsear fecha de creación
                created_at_str = row['Created at']
                try:
                    created_at = datetime.strptime(created_at_str, '%Y-%m-%d %H:%M:%S %z')
                except:
                    created_at = timezone.now()
                
                # Parsear fecha de entrega (fulfilled at)
                fulfilled_at_str = row['Fulfilled at']
                delivered_at = None
                if fulfilled_at_str:
                    try:
                        delivered_at = datetime.strptime(fulfilled_at_str, '%Y-%m-%d %H:%M:%S %z')
                    except:
                        delivered_at = timezone.now()
                
                # Guardar en diccionario
                orders_dict[order_number] = {
                    'order_id': order_id,
                    'order_number': order_number.replace('#', ''),  # Quitar el #
                    'customer_name': shipping_name,
                    'customer_email': shipping_email,
                    'customer_phone': shipping_phone,
                    'delivery_address': shipping_address,
                    'delivery_city': shipping_city,
                    'delivery_postal_code': shipping_zip,
                    'full_address': full_address,
                    'created_at': created_at,
                    'delivered_at': delivered_at,
                }
        
        # Crear pedidos en la base de datos
        created_count = 0
        skipped_count = 0
        
        for order_number, order_data in orders_dict.items():
            # Verificar si ya existe
            if Order.objects.filter(order_number=order_data['order_number']).exists():
                self.stdout.write(self.style.WARNING(f'⚠️  Pedido {order_number} ya existe, omitiendo...'))
                skipped_count += 1
                continue
            
            # Crear pedido
            order = Order.objects.create(
                order_number=order_data['order_number'],
                customer_name=order_data['customer_name'],
                customer_email=order_data['customer_email'],
                customer_phone=order_data['customer_phone'] or '',
                delivery_address=order_data['delivery_address'],
                delivery_city=order_data['delivery_city'],
                delivery_postal_code=order_data['delivery_postal_code'] or '',
                status='DELIVERED',
                current_location=f"Delivered to {order_data['delivery_city']}",
                delivered_at=order_data['delivered_at'],
                estimated_delivery=order_data['delivered_at'],
            )
            
            # Actualizar fecha de creación manualmente
            Order.objects.filter(pk=order.pk).update(created_at=order_data['created_at'])
            
            # Crear historial completo del pedido
            history_entries = [
                {
                    'status': 'PENDING',
                    'location': 'Order placed',
                    'description': 'Your order has been received and is being processed.',
                    'timestamp': order_data['created_at'],
                },
                {
                    'status': 'PROCESSING',
                    'location': 'Warehouse',
                    'description': 'Your order is being prepared for shipment.',
                    'timestamp': order_data['created_at'],
                },
                {
                    'status': 'SHIPPED',
                    'location': 'Origin facility',
                    'description': 'Your package has been shipped.',
                    'timestamp': order_data['created_at'],
                },
                {
                    'status': 'IN_TRANSIT',
                    'location': 'In transit',
                    'description': 'Your package is on its way.',
                    'timestamp': order_data['created_at'],
                },
                {
                    'status': 'OUT_FOR_DELIVERY',
                    'location': order_data['delivery_city'],
                    'description': 'Out for delivery in your area.',
                    'timestamp': order_data['delivered_at'] if order_data['delivered_at'] else order_data['created_at'],
                },
                {
                    'status': 'DELIVERED',
                    'location': order_data['full_address'],
                    'description': 'Package delivered successfully.',
                    'timestamp': order_data['delivered_at'] if order_data['delivered_at'] else order_data['created_at'],
                },
            ]
            
            for entry in history_entries:
                OrderHistory.objects.create(
                    order=order,
                    **entry
                )
            
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'✅ Pedido {order_number} importado correctamente'))
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Importación completada!'))
        self.stdout.write(self.style.SUCCESS(f'   📦 Pedidos creados: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'   ⏭️  Pedidos omitidos: {skipped_count}'))
        self.stdout.write(self.style.SUCCESS(f'   📊 Total procesados: {len(orders_dict)}'))
