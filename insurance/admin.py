from django.contrib import admin
from .models import Insurance, Modern


@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "policy_number",
        "policy_type",
        "provider",
        "premium",
        "start_date",
        "end_date",
        "policy_owner",
    )
    list_filter = ("provider", "policy_type", "start_date")
    search_fields = (
        "policy_number",
        "provider",
        "policy_type",
        "policy_owner__username",
        "policy_owner__email",
    )


admin.site.register(Modern)
