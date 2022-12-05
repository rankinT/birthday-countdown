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
    def __init__(self, text='', entity_id=None):
        """Initialize a Note object with the given text."""
        self.text = text

    def __str__(self):
        return self.text


class NoteManager():
    def __init__(self):
        self.note = Note()

    def save_note(self, entity):
        """Save a note to the datastore."""
        data_util.save_entity(entity)

    def update_note(self, text):
        """Update the text of a note."""
        self.note.text = clean(text)

        note_entity = self.fetch_note()
        note_entity['text'] = self.note.text

        self.save_note(note_entity)  # new note and entity from cleaned text

    def fetch_note(self):
        """Fetch the note for the user from the datastore."""
        return data_util.fetch_first_entity('note')

    def create_note(self):
        """Create a new note (only used if a note does not yet exist for the user)."""
        note_entity = data_util.create_entity('note')
        note_entity['text'] = ''
        self.save_note(note_entity)

        return note_entity

    def get_note(self):
        """Set up and return the note for the user."""
        note_entity = self.fetch_note()

        if not note_entity:
            # If a note hasn't yet been created for the user, create one.
            note_entity = self.create_note()

        self.note.text = note_entity['text']

        return self.note

    def clear_note(self):  # remove all notes
        """Clear the notes content."""
        self.update_note('')
