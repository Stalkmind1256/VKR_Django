from django.core.management.base import BaseCommand
from django.db import transaction
from fss.models import Category

CATEGORIES = [
    "technology",
    "education",
]

class Command(BaseCommand):
    help = 'Создаёт предустановленные категории.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        for category_name in CATEGORIES:
            obj, created = Category.objects.get_or_create(name=category_name)
            action = "Создана" if created else "Существует"
            self.stdout.write(f"{action}: {obj.name} — {dict(obj.CATEGORY_CHOICES).get(obj.name)}")
        self.stdout.write(self.style.SUCCESS("✅ Все категории успешно загружены."))
