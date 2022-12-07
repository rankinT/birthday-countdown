from google.cloud import datastore
from flask import session


def get_client():
    return datastore.Client()

def create_entity(kind):
    """Create a new entity of the given kind."""
    client = get_client()
    key = client.key(kind)
    return datastore.Entity(key)

def save_entity(entity):
    """Save an entity to datastore."""
    client = get_client()
    entity['user_email'] = session['email']
    client.put(entity)

def fetch_entity_list(kind):
    """Fetch all entities of the given kind."""
    client = get_client()
    query = client.query(kind=kind)
    query.add_filter('user_email', '=', session['email'])
    return [entity for entity in query.fetch()]

def fetch_first_entity(kind):
    """Fetch the first entity in an entity list of a given kind."""
    entities = fetch_entity_list(kind)
    if entities:
        return entities[0]
    else:
        return None

def fetch_by_id(kind, id):
    """Fetch an entity from datastore by its key"""
    client = get_client()
    key = client.key(kind, int(id))

    return client.get(key)

def delete_entity(kind, id):
    client = get_client()
    key = client.key(kind, int(id))
    client.delete(key)

def clear_user_entities(kind):
    client = get_client()
    entities = fetch_entity_list(kind)

    for entity in entities:
        key = client.key(kind, entity.id)
        client.delete(key)

def clear_all_entities(kind):
    client = get_client()
    query = client.query(kind=kind)

    for entity in query.fetch():
        key = client.key(kind, entity.id)
        client.delete(key)
