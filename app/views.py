from rest_framework import viewsets, status
from rest_framework.response import Response
from elasticsearch import Elasticsearch
from .models import Document
from .serializers import DocumentSerializer

es = Elasticsearch(['https://localhost:9200'])


class DocumentViewSet(viewsets.ViewSet):
    # Поиск документов
    def list(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response({"detail": "Query param 'query' is required."}, status=status.HTTP_400_BAD_REQUEST)

        response = es.search(index="documents", body={"query": {"match": {"content": query}}})
        doc_ids = [hit['_id'] for hit in response['hits']['hits']]
        documents = Document.objects.filter(id__in=doc_ids).order_by('-created_at')[:20]
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    # Удаление документа
    def destroy(self, request, pk=None):
        try:
            document = Document.objects.get(pk=pk)
            document.delete()
            es.delete(index="documents", id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Document.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
