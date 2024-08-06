import pytest
from django.utils import timezone
from core.models import User, Subscription
from core.tasks import send_birthday_notifications


@pytest.mark.django_db
def test_send_birthday_notifications(mailoutbox):
    today = timezone.now().date()
    user1 = User.objects.create_user(
        username="user1",
        email="user1@example.com",
        password="password123",
        birth_date=today,
    )
    user2 = User.objects.create_user(
        username="user2",
        email="user2@example.com",
        password="password123",
        birth_date=today,
    )
    subscription = Subscription.objects.create(user=user1, subscribed_to=user2)

    send_birthday_notifications()

    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "День рождение!"
    assert "Сегодня день рождение у пользователя - user2!" in mailoutbox[0].body
    assert mailoutbox[0].to == ["user1@example.com"]
