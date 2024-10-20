from celery import shared_task
from .models import Order

@shared_task
def process_order(order_id):
    try:
        order = Order.objects.get(id=order_id)
        
        order.total_price = sum(product.price for product in order.products.all())
        order.save()

    except Order.DoesNotExist:
        print(f'Order with id {order_id} does not exist.')
    except Exception as e:
        print(f'An error occurred while processing order {order_id}: {e}')

