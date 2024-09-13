from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from .models import Document
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://es:9200'])


class DocumentSearchView(View):
    def get(self, request):
        query = request.GET.get('q')
        documents = []

        if query:
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

        return render(request, 'index.html', {'documents': documents})


class DocumentDeleteView(View):
    def post(self, request, id):
        try:
            document = Document.objects.get(id=id)
            document.delete()  # Удаляем из базы данных
            es.delete(index='documents', id=id)  # Удаляем из Elasticsearch
            return redirect('document_search')  # Возврат на страницу поиска после удаления
        except Document.DoesNotExist:
            return JsonResponse({'error': 'Document not found'}, status=404)