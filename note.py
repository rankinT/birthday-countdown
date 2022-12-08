"""Classes and methods to manage a single user's note."""

import datetime
import data_util


def clean(s):
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('\n', ' ')
    s = s.replace('\t', ' ')
    s = s.strip()
    if len(s) > 100:
        s = s[:100]

    return s


class Note():
    def __init__(self, text='', entity_id=None, name=None):
        """Initialize a Note object with the given text."""
        self.text = text
        self.entity_id = entity_id
        self.name = name

    def __str__(self):
        return self.text


class NoteManager():
    def __init__(self):
        self.note = Note()

    def save_note(self, entity):
        """Save a note to the datastore."""
        data_util.save_entity(entity)

    def update_note(self, text, id):
        """Update the text of a note."""

        note_entity = self.fetch_note(id)
        note_entity['text'] = clean(text)

        self.note.text = note_entity['text']
        self.note.entity_id = note_entity.id
        self.note.name = note_entity['name']
    
        self.save_note(note_entity)  # new note and entity from cleaned text

    def fetch_note(self, id):
        """Fetch the note for the user from the datastore."""
        return data_util.fetch_by_id('note', id)

    def create_note(self, name):
        """Create a new note (only used if a note does not yet exist for the user)."""
        note_entity = data_util.create_entity('note')
        note_entity['text'] = ''
        note_entity['name'] = clean(name)
        self.save_note(note_entity)

        return note_entity

    def get_note(self, id, name=None):
        """Set up and return the note for the user."""
        note_entity = self.fetch_note(id)

        if not note_entity:
            # If a note hasn't yet been created for the user, create one.
            note_entity = self.create_note(name)

        self.note.text = note_entity['text']
        self.note.entity_id = note_entity.id
        self.note.name = note_entity['name']

        return self.note

    def delete_note(self, id):
        """Delete a note from the datastore"""
        data_util.delete_entity('note', id)
        
    def clear_note(self, note_id):  # remove all notes
        """Clear the notes content."""
        self.update_note('', note_id)
