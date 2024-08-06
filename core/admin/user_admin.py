from django.contrib import admin

from core.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "birth_date",
        "email",
    )
    list_filter = ("birth_date",)
    search_fields = (
        "id",
        "username",
        "email",
    )
    date_hierarchy = "birth_date"
