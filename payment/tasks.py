from io import BytesIO
from celery import shared_task,Task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order
from orders.tasks import RetryableTask


@shared_task(base=RetryableTask)
def payment_completed(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully paid.
 """
    try:
        order = Order.objects.get(id=order_id)
        subject = f'My Shop - Invoice no. {order.id}'
        message = 'Please, find attached the invoice for your recent purchase.'
        email = EmailMessage(subject,
                            message,
                            'teashop@technologynathan.com',
                            [order.email])
        # generate PDF
        html = render_to_string('orders/order/pdf.html', {'order': order})
        out = BytesIO()
        stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
        weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)

        # attach PDF file
        email.attach(f'order_{order.id}.pdf',out.getvalue(),'application/pdf')
        
        # send e-mail
        return email.send()
    
    except Exception as e:
        print(e)
        raise e

