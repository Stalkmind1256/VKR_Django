import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vkr.settings')
django.setup()
from django.contrib.auth.models import User
from fss.models import Status, Category


def create_statuses():
    """
    Функция для создания всех возможных статусов.
    """
    statuses = [
        ('pending', 'В ожидании'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]
    for code, name in statuses:
        # Проверяем, существует ли уже такой статус
        if not Status.objects.filter(status_name=name).exists():
            Status.objects.create(status_name=name)
            print(f"Статус '{name}' создан.")


def create_categories():
    """
    Функция для создания всех возможных категорий.
    """
    categories = [
        ('technology', 'Технологии'),
        ('education', 'Образование'),
    ]
    for code, name in categories:
        # Проверяем, существует ли уже такая категория
        if not Category.objects.filter(category_name=name).exists():
            Category.objects.create(category_name=name)
            print(f"Категория '{name}' создана.")


def create_admin_user():
    """
    Функция для создания пользователя с правами администратора.
    """
    username = 'admin'
    password = 'admin123'  # Очень простой пароль для тестов
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(username=username, password=password, email='admin@example.com')
        print(f"Администратор с именем '{username}' создан.")
    else:
        print(f"Администратор с именем '{username}' уже существует.")


# Основной скрипт
if __name__ == '__main__':
    create_statuses()
    create_categories()
    create_admin_user()
