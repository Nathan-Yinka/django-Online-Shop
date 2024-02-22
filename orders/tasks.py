from celery import shared_task, Task
from django.core.mail import send_mail
from .models import Order
import time

class RetryableTask(Task):
    autoretry_for = (Exception,)  # Retry for all exceptions
    max_retries = 3  # Maximum number of retries
    retry_backoff = True  # Enable exponential backoff

    def retry_policy(self, args, kwargs, exc_info):
        # Implement exponential backoff
        seconds_to_wait = 2 ** self.request.retries
        time.sleep(seconds_to_wait)

@shared_task(base=RetryableTask)
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Order nr. {order.id}'
        message = f'Dear {order.first_name},\n\n' \
                  f'You have successfully placed an order.' \
                  f'Your order ID is {order.id}.'

        mail_sent = send_mail(subject,
                              message,
                              'teashop@technologynathan.com',
                              [order.email])
        return mail_sent
    except Exception as e:
        print(e)
        # Log the exception or handle it as per your requirement
        # You can also raise the exception to let Celery handle retry
        raise e
