from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api_v0.serializers import SuggestionCreateSerializer
from fss.models import Status, Category, Suggestion


class SuggestionCreateModelViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'options', 'list']
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SuggestionCreateSerializer

    def get_queryset(self):
        return Suggestion.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def SuggestionCreateView(request):
    categories = Category.CATEGORY_CHOICES
    return render(request, 'api_v0/suggestion_create.html', {'categories': categories})
