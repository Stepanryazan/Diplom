from django.urls import path
from .views import DocumentViewSet

urlpatterns = [
    path('', DocumentViewSet.as_view({'get': 'list'})),
    path('', DocumentViewSet.as_view({'delete': 'destroy'})),
]
