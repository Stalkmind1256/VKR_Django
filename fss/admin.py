from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.contrib.auth.admin import UserAdmin

from .models import (
    Status,
    Category,
    Suggestion,
    Divisions,
    CustomUser,
    Role,
    Comment,
)

# ──────────────────────────── Roles ────────────────────────────
@admin.register(Role)
class RoleAdmin(ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    readonly_fields = ('id',)


# ────────────────────────── Categories ─────────────────────────
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name')
    readonly_fields = ('id',)
    fieldsets = (
        ('Основная информация', {'fields': ('name',)}),
    )


# ─────────────────────────── Suggestions ───────────────────────
class CommentInline(TabularInline):
    """Позволяет видеть/редактировать комментарии прямо в предложении."""
    model = Comment
    extra = 0
    fields = ('user', 'text', 'created_at')
    readonly_fields = ('created_at',)
    autocomplete_fields = ('user',)


@admin.register(Suggestion)
class SuggestionAdmin(ModelAdmin):
    list_display = ('id', 'title', 'user', 'category', 'status', 'date_create')
    readonly_fields = ('id', 'date_create')
    search_fields = ('title', 'description', 'id')           # ★ добавлено
    list_filter = ('category', 'status')                     # (необязательно, но удобно)
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'user', 'category', 'status', 'date_create')
        }),
    )
    inlines = [CommentInline]
    autocomplete_fields = ('user',)


# ─────────────────────────── Statuses ──────────────────────────
@admin.register(Status)
class StatusAdmin(ModelAdmin):
    list_display = ('id', 'name')
    readonly_fields = ('id',)
    search_fields = ('name',)
    fieldsets = (
        ('Основная информация', {'fields': ('name',)}),
    )


# ────────────────────────── Divisions ──────────────────────────
@admin.register(Divisions)
class DivisionAdmin(ModelAdmin):
    list_display = ('id', 'name')
    readonly_fields = ('id',)
    search_fields = ('name',)
    fieldsets = (
        ('Основная информация', {'fields': ('name',)}),
    )


# ─────────────────────────── Users ────────────────────────────
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'username', 'first_name', 'patronymic',
        'last_name', 'division', 'role', 'email', 'is_staff',
    )
    list_filter = ('division', 'role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')  # базовые поля UserAdmin
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личные данные', {
            'fields': ('first_name', 'patronymic', 'last_name', 'email', 'division', 'role')
        }),
        ('Права', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'first_name', 'patronymic', 'last_name',
                'division', 'role', 'password1', 'password2',
            ),
        }),
    )


# ─────────────────────────── Comments ─────────────────────────
@admin.register(Comment)
class CommentAdmin(ModelAdmin):
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
