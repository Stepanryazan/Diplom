from django.urls import path
from .views import DocumentSearchView, DocumentDeleteView

urlpatterns = [
    path('', DocumentSearchView.as_view(), name='document_search'),
    path('', DocumentDeleteView.as_view(), name='document_delete'),
]