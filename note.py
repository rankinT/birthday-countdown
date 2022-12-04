import datetime
import notedata

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
    def __init__(self,text):
        self.text = text

    def __str__(self):
        return '%s' % (self.text)

class NoteManager():
    def __init__(self):
        self.notes = []
        ent_list = notedata.fetch_entity_list()
        for ent in ent_list: #convert stored entities to notes
            note = Note(ent['text']) #create new note from ent['text'] data
            self.notes.append(note)

    def add_note(self,note):
        item = notedata.create_entity()
        item['text'] = note.text #add note's text AS ent's prop
        notedata.save_entity(item)

    def create_note(self,text):
        self.add_note(Note(clean(text))) #new note and entity from cleaned text

    def get_note_output(self):
        result = ''
        for ent in notedata.fetch_entity_list():
            note = Note(ent['text'])
            result = str(note)

        return result

    def clear_note(self): #remove all notes
        notedata.clear_note()
