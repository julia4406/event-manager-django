from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_event_registration_email(email, event_title):
    subject = f"Registration Confirmation for {event_title}"
    message = f"You have successfully registered for {event_title}!"
    from_email = None
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_event_cancel_email(email, event_title):
    subject = f"Registration Cancelled for {event_title}"
    message = f"Your registration for {event_title} has been cancelled."
    from_email = None
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

