from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

def send_order_email(order):
    subject = f'New Order #{order.id}'
    message = f'Order Details:\n\nCustomer: {order.customer.user.username}\nProduct: {order.product.name}\nQuantity: {order.quantity}\nOrder Date: {order.order_date}'
    
    # Get the single admin user
    admin = User.objects.filter(is_staff=True).first()
    if admin:
        recipient_list = [admin.email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

def send_order_sms(order):
    # Placeholder for SMS sending functionality
    pass