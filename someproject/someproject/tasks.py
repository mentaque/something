from celery import shared_task
from django.conf import settings
from django.core.mail import get_connection, EmailMessage


@shared_task
def send_email(email, code):
    with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
    ) as connection:
        subject = 'hello world'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        message = code
        EmailMessage(subject, message, email_from, recipient_list, connection=connection).send()