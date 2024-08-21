import elasticsearch
from app import es


def delete_by_id(index, id):
    try:
        es.delete(index=index, id=id)
        return True
    except elasticsearch.NotFoundError:
        return False


def query_index_by_text(index, text):
    search = es.search(
        index=index,
        size=20,
        query={'multi_match': {'query': text, 'fields': ['*']}})
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids


def query_index_by_id(index, id):
    result = es.search(index=index, size=1, query={
        "match": {
            'id': id
        }
    })["hits"]["hits"]
    return result


def add_to_index(index, model):
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    es.index(index=index, id=model.id, body=payload)
