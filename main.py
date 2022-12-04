from crypt import methods
import flask
import birthday
import note
from datetime import datetime


app = flask.Flask(__name__)
birthday_manager = birthday.BirthdayManager()
note_manager = note.NoteManager()


def update_countdown(note=None):
    today = datetime.strftime(datetime.today(), '%b %d, %Y')
    birthdays = birthday_manager.get_birthdays()
    return flask.render_template('index.html', birthdays=birthdays, today=today,note=note)


@app.route('/')
@app.route('/index.html')
def root():
    # Uncomment to clear database if there is an error:
    # birthday_manager.clear_birthdays()
    return update_countdown()

@app.route('/about.html')
def about_page():
    return flask.render_template('about.html', page_title='About This Application')


@app.route('/group-info.html')
def group_info_page():
    return flask.render_template('group-info.html', page_title='About This Application')


@app.route('/push', methods=['POST', 'GET'])
def push_birthday():
    name = flask.request.form['name']
    date = flask.request.form['date']

    #Only update birthdays if the form was filled completely
    if name and date: 
        formatted_date = datetime.strptime(date,'%Y-%m-%d')
        birthday_manager.create_birthday(name, formatted_date)
    
    return update_countdown()
    

@app.route('/delete-birthday', methods=['POST', 'GET'])
def delete_birthday_request():
    id = flask.request.values['id']
    birthday_manager.delete_birthday(id)

    return update_countdown()


@app.route('/clear-note', methods=['POST', 'GET'])
def clear_note_request():
    note_manager.clear_note()
    return update_countdown(note='')

@app.route('/load-note', methods=['POST', 'GET'])
def load_note_request():
    note = note_manager.get_note_output()
    return update_countdown(note)

@app.route('/save-note', methods=['POST', 'GET'])
def save_note_request():
    text = flask.request.form['note-area'] #get textarea
    note_manager.create_note(text)    
    return update_countdown(note='')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
