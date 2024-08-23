from django.urls import path
from .views import DocumentViewSet

urlpatterns = [
    path('documents/', DocumentViewSet.as_view({'get': 'list'})),
    path('documents/<int:pk>/', DocumentViewSet.as_view({'delete': 'destroy'})),
]
