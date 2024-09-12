from django.urls import path
from .views import DocumentSearchView, DocumentDeleteView

urlpatterns = [
    path('search/', DocumentSearchView.as_view(), name='document_search'),
    path('delete/<int:id>/', DocumentDeleteView.as_view(), name='document_delete')
]