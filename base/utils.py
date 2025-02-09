from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import africastalking

username = settings.AFRICASTALKING_USERNAME
api_key = settings.AFRICASTALKING_API_KEY
africastalking.initialize(username, api_key)
sms = africastalking.SMS


def send_order_email(order):
    subject = f'New Order #{order.id}'
    message = f'Order Details:\n\nCustomer: {order.customer.user.username}\nProduct: {order.product.name}\nQuantity: {order.quantity}\nOrder Date: {order.order_date}'
    
    # Get the single admin user
    admin = User.objects.filter(is_superuser=True).first()
    if admin:
        recipient_list = [admin.email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

def send_order_sms(order):
    # Placeholder for SMS sending functionality
            recipients = ["+254716067967"]
            # Set your message
            message = "Hey AT Ninja!";
            # Set your shortCode or senderId
            sender = 5313
            try:
                response = sms.send(message, recipients, sender)
                print (response)
            except Exception as e:
                print (f'Houston, we have a problem: {e}')

    


def send_message(message, recipients, sender):
        try:
            response = sms.send(message, recipients, sender)
            print("Message sent successfully:", response)
        except Exception as e:
            print(f"Error sending message: {e}")