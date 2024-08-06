import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from core.models import User, Subscription


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def _create_user(username, email, password, **kwargs):
        user = User.objects.create_user(
            username=username, email=email, password=password, **kwargs
        )
        user.save()
        return user

    return _create_user


@pytest.fixture
def auth_token(create_user):
    user = create_user(
        "testuser", "test@example.com", "password123", birth_date="1990-01-01"
    )
    token = RefreshToken.for_user(user)
    return str(token.access_token)


@pytest.mark.django_db
def test_authentication_required(api_client):
    response = api_client.get(reverse("users-list"))
    assert response.status_code == 401
    assert response.data["detail"] == "Authentication credentials were not provided."


@pytest.mark.django_db
def test_user_creation(api_client, auth_token):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")
    response = api_client.post(
        reverse("users-list"),
        {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "birth_date": "2000-01-01",
        },
        format="json",
    )
    assert response.status_code == 201
    assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_get_users(api_client, auth_token):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")
    response = api_client.get(reverse("users-list"))
    assert response.status_code == 200
    assert isinstance(response.data, list)


@pytest.mark.django_db
def test_get_user_detail(api_client, auth_token, create_user):
    user = create_user(
        "detailuser", "detail@example.com", "password123", birth_date="1990-01-01"
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")
    response = api_client.get(reverse("users-detail", kwargs={"pk": user.id}))
    assert response.status_code == 200
    assert response.data["username"] == "detailuser"


@pytest.mark.django_db
def test_subscription_creation(api_client, auth_token, create_user):
    user = create_user(
        "otheruser", "other@example.com", "password123", birth_date="1990-01-01"
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")
    response = api_client.post(
        reverse("subscriptions-list"), {"subscribed_to": user.id}, format="json"
    )
    assert response.status_code == 201
    assert Subscription.objects.filter(
        user__username="testuser", subscribed_to=user
    ).exists()


@pytest.mark.django_db
def test_prevent_self_subscription(api_client, auth_token):
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")
    response = api_client.post(
        reverse("subscriptions-list"),
        {"subscribed_to": User.objects.get(username="testuser").id},
        format="json",
    )
    assert response.status_code == 400
    assert "Вы не можете подписаться на себя." in response.data["non_field_errors"]


@pytest.mark.django_db
def test_duplicate_subscription(api_client, auth_token, create_user):
    user = create_user(
        "otheruser", "other@example.com", "password123", birth_date="1990-01-01"
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")

    # Первая подписка
    response = api_client.post(
        reverse("subscriptions-list"), {"subscribed_to": user.id}, format="json"
    )
    assert response.status_code == 201

    # повторная подписка
    response = api_client.post(
        reverse("subscriptions-list"), {"subscribed_to": user.id}, format="json"
    )
    assert response.status_code == 400
    assert (
        "Вы уже подписаны на этого пользователя." in response.data["non_field_errors"]
    )


@pytest.mark.django_db
def test_delete_subscription(api_client, auth_token, create_user):
    user = create_user(
        "otheruser", "other@example.com", "password123", birth_date="1990-01-01"
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_token}")

    # Создаем подписку
    response = api_client.post(
        reverse("subscriptions-list"), {"subscribed_to": user.id}, format="json"
    )
    assert response.status_code == 201

    subscription_id = Subscription.objects.get(
        user__username="testuser", subscribed_to=user
    ).id

    # Удаляем подписку
    response = api_client.delete(
        reverse("subscriptions-detail", kwargs={"pk": subscription_id})
    )
    assert response.status_code == 204
    assert not Subscription.objects.filter(
        user__username="testuser", subscribed_to=user
    ).exists()
