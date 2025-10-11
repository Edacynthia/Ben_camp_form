from django.core.management.base import BaseCommand
from camp_form.models import CampRegistration


class Command(BaseCommand):
    help = "Reset all registration IDs to sequential numbers"

    def add_arguments(self, parser):
        parser.add_argument(
            "--confirm",
            action="store_true",
            help="Confirm that you want to reset all registration IDs",
        )

    def handle(self, *args, **options):
        if not options["confirm"]:
            self.stdout.write(
                self.style.WARNING(
                    "This will reset all registration IDs to sequential numbers (1, 2, 3, etc.)\n"
                    "Use --confirm to proceed."
                )
            )
            return

        # Get all registrations ordered by creation date
        registrations = CampRegistration.objects.order_by("created_at")

        updated_count = 0
        for index, registration in enumerate(registrations, start=1):
            old_id = registration.registration_id
            registration.registration_id = str(index)
            registration.save(update_fields=["registration_id"])
            updated_count += 1
            self.stdout.write(f"Updated {old_id} -> {index}")

        self.stdout.write(
            self.style.SUCCESS(f"Successfully updated {updated_count} registration IDs")
        )
