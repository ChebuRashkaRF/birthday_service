from celery import shared_task
from django.utils import timezone
from .models import User


@shared_task
def send_birthday_notifications():
    today = timezone.now().date()
    users_with_birthdays = User.objects.filter(
        birth_date__month=today.month, birth_date__day=today.day
    ).prefetch_related("subscribers")

    emails = []
    for user in users_with_birthdays:
        for subscription in user.subscribers.all():
            message = f"Сегодня день рождение у пользователя - {user.username}!"
            emails.append(
                {
                    "subject": "День рождение!",
                    "message": message,
                    "from_email": None,
                    "recipient_list": [subscription.user.email],
                }
            )

    # Отправка всех писем
    send_bulk_emails(emails)


def send_bulk_emails(emails):
    from django.core.mail import send_mass_mail

    email_tuples = [
        (
            email["subject"],
            email["message"],
            email["from_email"],
            email["recipient_list"],
        )
        for email in emails
    ]
    send_mass_mail(email_tuples, fail_silently=False)
