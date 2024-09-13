from elasticsearch import Elasticsearch

es = Elasticsearch(['http://es:9200'])

def create_index():
    es.indices.create(
        index='documents',
        body={
            'mappings': {
                'properties': {
                    'id': {'type': 'integer'},
                    'text': {'type': 'text'},
                }
            }
        },
        ignore=400  # Игнорировать ошибку, если индекс уже существует
    )