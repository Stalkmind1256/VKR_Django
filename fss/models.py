from django.db import models
from django.contrib.auth.models import User


#Статусы
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

#Категории
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


#Структруные подразделения
class Divisions(models.Model):
    DIVISIONS_CHOICES = [
        ('technopark', 'Технопарк'),
        ('deanery', 'Деканат'),
        ('rectorate', 'Ректорат'),
        ('uvc', 'Учебно-вычислительный центр (УВЦ)'),
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
        ordering = ["name"]  # Сортировка по алфавиту

    def __str__(self):
        return self.get_name_display()



#Предложения
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
    division = models.ForeignKey(
        'Divisions',  # Связь с моделью Divisions
        on_delete=models.PROTECT,
        null=True,
        related_name='suggestions',  # Позволяет получить все предложения для определенного подразделения
        verbose_name='Подразделение',  # Подразделение, к которому относится предложение
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



class Comment(models.Model):
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.user.username} к {self.suggestion.title}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
# class Role(models.Model):
#     user = models.OneToOneField(User, on_delete=models.PROTECT)
#     role_name = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('user', 'User')], default='user')
#
#     def __str__(self):
#         return f"{self.user.username} - {self.role_name}"
class SuggestionRating(models.Model):
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # от 1 до 5, например

    class Meta:
        unique_together = ('suggestion', 'user')  # один пользователь — одна оценка