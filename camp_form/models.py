from django.db import models
import uuid


class ServiceUnit(models.Model):
    """Model for service units that users can select from"""

    name = models.CharField(max_length=100, unique=True, verbose_name="Unit Name")
    description = models.TextField(blank=True, verbose_name="Description")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Service Unit"
        verbose_name_plural = "Service Units"
        ordering = ["name"]

    def __str__(self):
        return self.name


class CampRegistration(models.Model):
    """Model for storing BEN Camp Meeting registration data"""

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    YES_NO_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
    ]

    # Basic Information
    fullname = models.CharField(max_length=255, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, verbose_name="Gender"
    )

    # Camp-specific Information
    can_pay = models.CharField(
        max_length=3, choices=YES_NO_CHOICES, verbose_name="Can Pay for Camp Meeting"
    )
    work_units = models.ManyToManyField(
        ServiceUnit, verbose_name="Work Units", help_text="Select the units you work in"
    )

    # Health Information
    allergies = models.CharField(
        max_length=3, choices=YES_NO_CHOICES, verbose_name="Has Allergies"
    )
    health_challenges = models.CharField(
        max_length=3, choices=YES_NO_CHOICES, verbose_name="Has Health Challenges"
    )

    # Travel and Emergency
    arrival_departure = models.TextField(verbose_name="Arrival and Departure Plan")
    emergency_contact = models.TextField(verbose_name="Emergency Contact Information")

    # System Fields
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Registration Date"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        verbose_name = "Camp Registration"
        verbose_name_plural = "Camp Registrations"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.fullname} - {self.pk}"
