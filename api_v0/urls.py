from django.urls import path, include
from rest_framework import routers
from .views import SuggestionCreateModelViewSet, SuggestionCreateView

router = routers.DefaultRouter()
router.register(prefix=r'suggestion', viewset=SuggestionCreateModelViewSet, basename='suggestion')


urlpatterns = [
    path('create-suggestion', SuggestionCreateView)
]

urlpatterns += path('', include(router.urls)),

