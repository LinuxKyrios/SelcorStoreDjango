from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_created(order_id):
    """
    Task sending notifications through email after finished order
    """
    order = Order.objects.get(id=order_id)
    subject = 'Zamówienie nr {}'.format(order.id)
    message = 'Witaj, {}!\n\n Złożyłeś zamówienie w naszym sklepie.' \
              'Identyfikator zamówienia to {}.'.format(order.first_name, order.id)
    mail_sent = send_mail(subject,
                          message,
                          'admin@selcorstore.pl',
                          [order.email])
    return mail_sent