from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Avg  # 💡 Добавлен для avg_rating property
from django.contrib.auth import get_user_model


class Divisions(models.Model):
    DIVISIONS_CHOICES = [
        ('technopark', 'Технопарк'),
        ('deanery', 'Деканат'),
        ('rectorate', 'Ректорат'),
        ('uvc', 'Учебно-вычислительный центр (УВЦ)'),
        ('administration', 'Администрация'),
    ]

    name = models.CharField(
        max_length=100,
        choices=DIVISIONS_CHOICES,
        unique=True,
        verbose_name="Название подразделения"
    )

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"
        ordering = ["name"]

    def __str__(self):
        return self.get_name_display()


class CustomUser(AbstractUser):
    patronymic = models.CharField("Отчество", max_length=150, blank=True, null=True)
    division = models.ForeignKey(
        Divisions,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Подразделение"
    )


class Status(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('submitted', 'Отправлено'),
        ('under_review', 'На рассмотрении'),
        ('approved', 'Подтверждено'),
        ('preparing', 'Готовится к реализации'),
        ('in_progress', 'Реализуется'),
        ('completed', 'Реализовано'),
        ('rejected', 'Отклонено'),
        ('archived', 'Архив'),
    ]
    name = models.CharField(
        max_length=200,
        choices=STATUS_CHOICES,
        verbose_name='Название статуса',
    )

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['name']

    def __str__(self):
        return dict(self.STATUS_CHOICES).get(self.name, self.name)


class Category(models.Model):
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
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()


class Suggestion(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
        ordering = ['-date_create']

    def __str__(self):
        return self.title

    @property
    def avg_rating(self):
        avg = self.ratings.aggregate(avg=Avg('rating'))['avg']
        return round(avg or 0, 1)

    @property
    def votes_count(self):
        return self.ratings.count()

    def can_change_status(self, new_status_name):
        transitions = {
            'draft': ['submitted'],  # черновик → отправлено
            'submitted': ['under_review', 'archived', 'draft'],
            # отправлено → на рассмотрении, архив или возврат в черновик
            'under_review': ['approved', 'rejected'],  # на рассмотрении → подтверждено или отклонено
            'approved': ['preparing'],  # подтверждено → готовится к реализации
            'preparing': ['in_progress'],  # готовится → реализуется
            'in_progress': ['completed'],  # реализуется → реализовано
            'completed': [],  # завершено — конец
            'rejected': ['archived', 'draft'],  # отклонено → архив или возврат в черновик
            'archived': [],  # архив — конец
        }

        current = self.status.name
        allowed = transitions.get(current, [])
        return new_status_name in allowed




class Comment(models.Model):
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.user.username} к {self.suggestion.title}"


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class SuggestionRating(models.Model):
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        unique_together = ('suggestion', 'user')
