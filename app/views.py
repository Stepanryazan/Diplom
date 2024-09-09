from django.http import JsonResponse
from django.views import View
from .models import Document
from elasticsearch import Elasticsearch

es = Elasticsearch(['https://localhost:9200'])

class DocumentSearchView(View):
    def get(self, request):
        query = request.GET.get('q')
        if not query:
            return JsonResponse({'error': 'Query parameter is required'}, status=400)

        # Поиск в Elasticsearch
        search_results = es.search(
            index='documents',
            body={
                'query': {
                    'match': {
                        'text': query
                    }
                }
            },
            size=20  # Ограничиваемся 20 результатами
        )

        doc_ids = [hit['_source']['id'] for hit in search_results['hits']['hits']]
        documents = Document.objects.filter(id__in=doc_ids)

        # Формируем ответ
        response_data = {
            'documents': [{'id': doc.id, 'rubrics': doc.rubrics, 'text': doc.text, 'created_date': doc.created_date} for doc in documents]
        }
        return JsonResponse(response_data, safe=False)

class DocumentDeleteView(View):
    def delete(self, request, id):
        try:
            document = Document.objects.get(id=id)
            document.delete()  # Удаляем из базы данных
            es.delete(index='documents', id=id)  # Удаляем из Elasticsearch
            return JsonResponse({'success': True}, status=204)
        except Document.DoesNotExist:
            return JsonResponse({'error': 'Document not found'}, status=404)