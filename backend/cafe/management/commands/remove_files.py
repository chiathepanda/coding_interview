import shutil

from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Deletes all __pycache__ folders and migration files (except __init__.py)'

    def handle(self, *args, **options):
        base_dir = Path(settings.BASE_DIR)

        # Delete all __pycache__ folders
        for pycache in base_dir.rglob('__pycache__'):
            try:
                shutil.rmtree(pycache)
                self.stdout.write(self.style.SUCCESS(f'Deleted {pycache}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to delete {pycache}: {e}'))

        # Delete all migration files except __init__.py in the migrations folders
        for migrations_folder in base_dir.rglob('migrations'):
            try:
                # Skip if no migration files are present (excluding __init__.py)
                if not any(migrations_folder.glob('[!__init__]*.py')):
                    continue

                # Delete all files in the migrations folder except __init__.py
                for item in migrations_folder.iterdir():
                    if item.name != '__init__.py':
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item)
                self.stdout.write(self.style.SUCCESS(f'Cleaned {migrations_folder}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to clean {migrations_folder}: {e}'))

        self.stdout.write(self.style.SUCCESS('All __pycache__ and migration folders have been cleaned.'))
