from django.core.mail import send_mail
from django.conf import settings

def send_order_email(order):
    subject = f'New Order #{order.id}'
    message = f'Order Details:\n\nCustomer: {order.customer.user.username}\nProduct: {order.product.name}\nQuantity: {order.quantity}\nOrder Date: {order.order_date}'
    recipient_list = [order.product.admin.email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

def send_order_sms(order):
    # Placeholder for SMS sending functionality
    pass