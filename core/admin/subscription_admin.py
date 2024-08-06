from django.contrib import admin

from core.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "subscribed_to",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = (
        "user_id",
        "user__email",
        "subscribed_to_id",
        "subscribed_to__email",
    )
    date_hierarchy = "created_at"

    raw_id_fields = ("user", "subscribed_to")

    list_select_related = ("user", "subscribed_to")
