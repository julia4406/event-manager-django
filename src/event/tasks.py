from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_event_registration_email(email, event_title):
    subject = f"Registration Confirmation for {event_title}"
    message = f"You have successfully registered for {event_title}!"
    from_email = None
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
