from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Status, Category, Suggestion, Divisions


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'name')
    readonly_fields = ('id',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('name',)
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
    list_display = ('id', 'name')  # Отображаем id и имя подразделения
    readonly_fields = ('id',)  # Поле id только для чтения
    search_fields = ('name',)  # Добавляем поиск по названию подразделения
    fieldsets = (
        ('Основная информация', {
            'fields': ('name',)
        }),
    )