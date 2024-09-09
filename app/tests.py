from django.test import TestCase
from django.urls import reverse
from .models import Document
from elasticsearch import Elasticsearch
from rest_framework import status


class DocumentTests(TestCase):

    def setUp(self):
        self.es = Elasticsearch()
        self.doc1 = Document.objects.create(
            rubrics=["rubric1", "rubric2"],
            text="Текст документа 1"
        )
        self.doc2 = Document.objects.create(
            rubrics=["rubric2", "rubric3"],
            text="Текст документа 2"
        )

        # Индексируем документы в Elasticsearch
        self.index_document(self.doc1)
        self.index_document(self.doc2)

    def index_document(self, document):
        self.es.index(index='documents', id=document.id, body={
            'id': document.id,
            'text': document.text,
        })

    def test_document_search(self):
        response = self.client.get(reverse('document_search'), {'q': 'Текст'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('documents', response.data)
        self.assertEqual(len(response.data['documents']), 2)  # Два документа должны найтись

        response = self.client.get(reverse('document_search'), {'q': 'документ 1'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['documents']), 1)  # Только один документ

    def test_document_delete(self):
        # Подсчитываем количество документов перед удалением
        self.assertEqual(Document.objects.count(), 2)

        response = self.client.delete(reverse('document_delete', args=[self.doc1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что документ удален из базы данных
        self.assertEqual(Document.objects.count(), 1)

        # Проверяем, что документ удален из Elasticsearch
        es_response = self.es.get(index='documents', id=self.doc1.id, ignore=404)
        self.assertNotIn(self.doc1.id, es_response)

    def tearDown(self):
        self.doc1.delete()
        self.doc2.delete()
        self.es.indices.delete(index='documents', ignore=[400, 404])  # Удаляем индекс после тестов