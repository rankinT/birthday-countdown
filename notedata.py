from google.cloud import datastore


def get_client():
    return datastore.Client()

def create_entity():
    client = get_client()
    key = client.key('note')  # create key
    return datastore.Entity(key)   # return new entity from key

def save_entity(entity):
    client = get_client()
    client.put(entity)  # store entity to gcloud

def fetch_entity_list():
    client = get_client()
    query = client.query(kind='note')
    result = []
    for entity in query.fetch():
        result.append(entity)
    return result #list of entities... of kind 'note'


def clear_note():
    client = get_client()
    query = client.query(kind='note') #query entities of kind 'note'

    for entity in query.fetch():
        key = client.key('note', entity.id)  # get entity key from kind,id
        client.delete(key)  # delete entity from its unique key
