from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from .models import Status, Category, Suggestion, Divisions, CustomUser,Role, Comment

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Подставьте реальные поля вашей модели Role
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name')
    readonly_fields = ('id',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('name',)  # Поле name — обычное текстовое поле
        }),
    )


@admin.register(Suggestion)
class SuggestionAdmin(ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'status', 'date_create')
    readonly_fields = ('id', 'date_create')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'user', 'category', 'status', 'date_create')
        }),
    )


@admin.register(Status)
class StatusAdmin(ModelAdmin):
    list_display = ('id', 'name')
    readonly_fields = ('id',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('name',)
        }),
    )


@admin.register(Divisions)
class DivisionAdmin(ModelAdmin):
    list_display = ('id', 'name')
    readonly_fields = ('id',)
    search_fields = ('name',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('name',)
        }),
    )


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('username', 'first_name', 'patronymic', 'last_name', 'division', 'role', 'email', 'is_staff')
    list_filter = ('division', 'role', 'is_staff', 'is_superuser', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личные данные', {'fields': ('first_name', 'patronymic', 'last_name', 'email', 'division', 'role')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'patronymic', 'last_name', 'division', 'role', 'password1', 'password2'),
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'suggestion', 'user', 'short_text', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('text', 'user__username', 'suggestion__title')
    autocomplete_fields = ('suggestion', 'user')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    def short_text(self, obj):
        """
        Возвращает первые 75 символов текста комментария
        (добавляет многоточие, если строка длиннее).
        """
        return f"{obj.text[:75]}…" if len(obj.text) > 75 else obj.text

    short_text.short_description = 'Текст'
