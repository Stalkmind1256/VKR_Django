from django.core.management.base import BaseCommand
from django.db import transaction
from fss.models import Category

CATEGORIES = [
    "Технологии",
    "Образование",
    "Наука",
    "Инфраструктура",
]

class Command(BaseCommand):
    help = 'Создаёт предустановленные категории.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        for category_name in CATEGORIES:
            obj, created = Category.objects.get_or_create(name=category_name)
            action = "Создана" if created else "Существует"
            self.stdout.write(f"{action}: {obj.name}")
        self.stdout.write(self.style.SUCCESS("✅ Все категории успешно загружены."))