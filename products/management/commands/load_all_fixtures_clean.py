# products/management/commands/load_all_fixtures_clean.py

import os
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Flushes DB, re-applies migrations, and loads all fixtures cleanly."

    def handle(self, *args, **options):
        confirm = input("\nThis will FLUSH your database and reload all fixtures. Are you sure? (yes/no): ")
        if confirm.lower() != 'yes':
            self.stdout.write(self.style.WARNING("Aborted by user."))
            return

        self.stdout.write(self.style.WARNING("\n>> Flushing database..."))
        call_command("flush", interactive=False)

        self.stdout.write(self.style.SUCCESS("\n>> Running migrations..."))
        call_command("migrate")

        fixtures = [
            "initial_data",              # categories and dietary tags
            "products_data_cleaned",     # corrected products fixture
        ]

        for fixture in fixtures:
            self.stdout.write(self.style.WARNING(f"\n>> Loading fixture: {fixture}.json"))
            try:
                call_command("loaddata", fixture)
                self.stdout.write(self.style.SUCCESS(f"✅ Loaded: {fixture}.json"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"❌ Error loading {fixture}.json: {e}"))

        self.stdout.write(self.style.SUCCESS("\n🎉 All fixtures loaded cleanly."))

