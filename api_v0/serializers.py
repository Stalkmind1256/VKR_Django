from rest_framework.serializers import ModelSerializer
from fss.models import Status, Category, Suggestion


class SuggestionCreateSerializer(ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ['title', 'description', 'category']
        extra_kwargs = {
            "title": {
                "error_messages": {"required": "Укажите название.", "blank": "Пожалуйста, заполните поле названия."}
            },
            "description": {
                "error_messages": {"required": "Введите описание.", "blank": "Пожалуйста, заполните поле описания."}
            },
            "category": {
                "error_messages": {"required": "Укажите категорию.", "blank": "Пожалуйста, выберите категорию."}
            },
        }

    def create(self, validated_data):
        pending_status = Status.objects.get(name='pending')
        user = self.context['request'].user
        suggestion = Suggestion.objects.create(
            user=user,
            title=validated_data['title'],
            description=validated_data['description'],
            category=validated_data.get('category'),  # Исправлено
            status=pending_status,
        )
        return suggestion
