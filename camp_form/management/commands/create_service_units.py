from django.core.management.base import BaseCommand
from camp_form.models import ServiceUnit


class Command(BaseCommand):
    help = "Create initial service units"

    def handle(self, *args, **options):
        units = [
            "Media Unit",
            "Technical Unit",
            "Secretariat Unit",
            "Event Planning",
            "Pastoral Care",
            "Publication Unit",
            "Library Unit",
            "Medical Unit",
            "Transport Unit",
            "Academic Unit",
            "ICT Unit",
            "Hospitality Unit",
            "Ushering Unit",
            "Finance Unit",
            "Business Unit",
        ]

        created_count = 0
        for unit_name in units:
            unit, created = ServiceUnit.objects.get_or_create(
                name=unit_name, defaults={"is_active": True}
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created service unit: {unit_name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Service unit already exists: {unit_name}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {created_count} new service units"
            )
        )
