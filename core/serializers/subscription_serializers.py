from rest_framework import serializers

from ..models import Subscription


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["subscribed_to", "created_at"]

    def validate(self, data):
        user = self.context["request"].user
        subscribed_to = data["subscribed_to"]

        if user == subscribed_to:
            raise serializers.ValidationError("Вы не можете подписаться на себя.")

        if Subscription.objects.filter(user=user, subscribed_to=subscribed_to).exists():
            raise serializers.ValidationError("Вы уже подписаны на этого пользователя.")

        return data


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "user", "subscribed_to", "created_at"]
