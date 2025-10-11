from django.db import models
import uuid


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
    work_unit = models.CharField(max_length=255, verbose_name="Work Unit")

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
    registration_id = models.CharField(
        max_length=100, unique=True, editable=False, verbose_name="Registration ID"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Registration Date"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        verbose_name = "Camp Registration"
        verbose_name_plural = "Camp Registrations"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        """Generate a unique registration ID if not already set"""
        if not self.registration_id:
            # Generate a simple numeric ID based on timestamp and random component
            import time
            import random

            timestamp = str(int(time.time()))[-6:]  # Last 6 digits of timestamp
            random_num = str(random.randint(100, 999))
            self.registration_id = f"BEN{timestamp}{random_num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fullname} - {self.registration_id}"
