from django.contrib import admin
from .models import CampRegistration, ServiceUnit


@admin.register(ServiceUnit)
class ServiceUnitAdmin(admin.ModelAdmin):
    """Admin interface for Service Unit model"""

    list_display = ["name", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "description"]
    list_editable = ["is_active"]
    readonly_fields = ["created_at"]

    fieldsets = (
        ("Unit Information", {"fields": ("name", "description", "is_active")}),
        ("System Information", {"fields": ("created_at",), "classes": ("collapse",)}),
    )


@admin.register(CampRegistration)
class CampRegistrationAdmin(admin.ModelAdmin):
    """Admin interface for Camp Registration model"""

    def get_work_units_display(self, obj):
        """Display work units as a comma-separated string"""
        return ", ".join([unit.name for unit in obj.work_units.all()])

    get_work_units_display.short_description = "Work Units"

    list_display = [
        "pk",
        "fullname",
        "email",
        "phone",
        "gender",
        "can_pay",
        "get_work_units_display",
        "created_at",
    ]

    list_filter = [
        "gender",
        "can_pay",
        "allergies",
        "health_challenges",
        "created_at",
        "work_units",
    ]

    search_fields = ["fullname", "email", "phone"]

    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("Basic Information", {"fields": ("fullname", "email", "phone", "gender")}),
        ("Camp Information", {"fields": ("can_pay", "work_units")}),
        ("Health Information", {"fields": ("allergies", "health_challenges")}),
        ("Travel & Emergency", {"fields": ("arrival_departure", "emergency_contact")}),
        (
            "System Information",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    ordering = ["-created_at"]
