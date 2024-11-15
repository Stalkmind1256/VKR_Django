from django.db import models
from django.contrib.auth.models import User


class Status(models.Model):
    """
    Модель для статусов предложений.
    """
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено')
    ]
    name = models.CharField(
        max_length=200,
        choices=STATUS_CHOICES,
        verbose_name='Название статуса',
    )

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['name']  # Сортировка по алфавиту

    def __str__(self):
        return dict(self.STATUS_CHOICES).get(self.name, self.name)


class Category(models.Model):
    """
    Модель для категорий предложений.
    """
    CATEGORY_CHOICES = [
        ('technology', 'Технологии'),
        ('education', 'Образование'),
    ]
    name = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        verbose_name='Название категории',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']  # Сортировка по алфавиту

    def __str__(self):
        return self.get_name_display()  # Возвращает читаемое название категории


class Suggestion(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='suggestions',
        verbose_name='Пользователь',
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Название',
    )
    description = models.TextField(
        max_length=10000,
        verbose_name='Описание',
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        null=True,
        related_name='suggestions',
        verbose_name='Категория',
    )
    status = models.ForeignKey(
        'Status',
        on_delete=models.PROTECT,
        null=True,
        related_name='suggestions',
        verbose_name='Статус',
    )
    date_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'
        ordering = ['-date_create']  # Сортировка по дате создания (от последнего к первому)

    def __str__(self):
        return self.title

# class Role(models.Model):
#     user = models.OneToOneField(User, on_delete=models.PROTECT)
#     role_name = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('user', 'User')], default='user')
#
#     def __str__(self):
#         return f"{self.user.username} - {self.role_name}"
