from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from fss.models import Divisions  # импортируем модель подразделений


class Command(BaseCommand):
    help = 'Создаёт суперпользователя (админа) с заполненными ФИО и подразделением, если его нет.'

    def handle(self, *args, **options):
        User = get_user_model()

        username = 'admin'
        email = 'admin@example.com'
        password = 'admin'  # менять обязательно!

        try:
            division = Divisions.objects.get(name='administration')  # имя из choices должно совпадать
        except Divisions.DoesNotExist:
            division = None
            self.stdout.write(self.style.WARNING('Подразделение "Администрация" не найдено.'))

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.WARNING('Суперпользователь уже существует.'))
        else:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Дмитрий',
                last_name='Гордиевских',
            )
            # поле patronymic и division — возможно, нужно присвоить отдельно
            user.patronymic = 'Михайлович'
            if division:
                user.division = division
            user.save()

            self.stdout.write(self.style.SUCCESS(f'Суперпользователь {username} создан с ФИО и подразделением.'))
