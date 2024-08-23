from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Document


class DocumentAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.document_1 = Document.objects.create(title='Test Document 1',
                                                  content='This is the content of test document 1.')
        self.document_2 = Document.objects.create(title='Test Document 2',
                                                  content='This content is for test document 2.')

    def test_search_documents(self):
        response = self.client.get('/api/documents/', {'query': 'test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Ожидаем, что вернется 2 документа
        self.assertIn('Test Document 1', [doc['title'] for doc in response.data])
        self.assertIn('Test Document 2', [doc['title'] for doc in response.data])

    def test_search_documents_no_result(self):
        response = self.client.get('/api/documents/', {'query': 'nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Ожидаем, что ничего не вернется

    def test_delete_document(self):
        response = self.client.delete(f'/api/documents/{self.document_1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Document.objects.count(), 1)  # Ожидаем, что осталось 1 документ

        # Проверяем, что документ был действительно удален
        response = self.client.get('/api/documents/', {'query': 'test'})
        self.assertEqual(len(response.data), 1)
        self.assertIn('Test Document 2', [doc['title'] for doc in response.data])

    def test_delete_nonexistent_document(self):
        response = self.client.delete('/api/documents/999/')  # Предполагаем, что такого документа нет
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)