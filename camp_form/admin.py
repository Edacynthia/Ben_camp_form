from django.contrib import admin
from .models import CampRegistration


@admin.register(CampRegistration)
class CampRegistrationAdmin(admin.ModelAdmin):
    """Admin interface for Camp Registration model"""

    list_display = [
        "registration_id",
        "fullname",
        "email",
        "phone",
        "gender",
        "can_pay",
        "created_at",
    ]

    list_filter = ["gender", "can_pay", "allergies", "health_challenges", "created_at"]

    search_fields = ["fullname", "email", "phone", "registration_id", "work_unit"]

    readonly_fields = ["registration_id", "created_at", "updated_at"]

    fieldsets = (
        ("Basic Information", {"fields": ("fullname", "email", "phone", "gender")}),
        ("Camp Information", {"fields": ("can_pay", "work_unit")}),
        ("Health Information", {"fields": ("allergies", "health_challenges")}),
        ("Travel & Emergency", {"fields": ("arrival_departure", "emergency_contact")}),
        (
            "System Information",
            {
                "fields": ("registration_id", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    ordering = ["-created_at"]
