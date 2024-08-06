from rest_framework.routers import DefaultRouter

from core.viewsets import UserViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"subscriptions", SubscriptionViewSet, basename="subscriptions")
