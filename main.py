from flask import Flask, session, url_for, render_template, redirect, request
import birthday
import note
from datetime import datetime
from auth import auth as auth_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bday'
app.register_blueprint(auth_blueprint)

# Global variables for managing the state of the site
birthday_manager = birthday.BirthdayManager()
note_manager = note.NoteManager()


@app.route('/')
@app.route('/index.html')
def root():
    # Uncomment to clear database if there is an error:
    # birthday_manager.clear_birthdays()
    
    if not session.get('loggedin'):
        return redirect(url_for('auth.login'))

    birthdays = birthday_manager.get_birthdays()
    today = datetime.strftime(datetime.today(), '%b %d, %Y')

    if birthdays:
        note_id = session.get('note_id')
        note_name = session.get('note_name')
        if note_id and note_name:
            note = note_manager.get_note(note_id, note_name)
        else:
            first_note_id = birthdays[0].note_id
            first_note_name = birthdays[0].name
            note = note_manager.get_note(first_note_id, first_note_name)  
    else:
        note = None  

    return render_template('index.html', birthdays=birthdays, today=today, note=note, page_title='Home')


@app.route('/about.html')
def about_page():
    return render_template('about.html', page_title='About')


@app.route('/group-info.html')
def group_info_page():
    return render_template('group-info.html', page_title='Group Info')


@app.route('/push', methods=['POST', 'GET'])
def push_birthday():
    name = request.form['name']
    date = request.form['date']

    # Only update birthdays if the form was filled completely
    if name and date:
        formatted_date = datetime.strptime(date, '%Y-%m-%d')
        birthday_manager.create_birthday(name, formatted_date)

    return redirect(url_for('root'))


@app.route('/delete-birthday', methods=['POST', 'GET'])
def delete_birthday_request():
    id = request.values['id']
    note_id = request.values['note_id']
    note_manager.delete_note(note_id)
    birthday_manager.delete_birthday(id)

    return redirect(url_for('root'))



@app.route('/clear-note', methods=['POST', 'GET'])
def clear_note_request():
    note_id = request.form['note_id']
    note_manager.clear_note(note_id)

    return redirect(url_for('root'))


@app.route('/discard-note-changes', methods=['POST', 'GET'])
def discard_note_changes_request():

    return redirect(url_for('root'))


@app.route('/save-note', methods=['POST', 'GET'])
def save_note_request():
    text = request.form['note-area']  # get textarea
    note_id = request.form['note_id']
    note_manager.update_note(text, note_id)
    
    return redirect(url_for('root'))


@app.route('/change-note', methods=['POST', 'GET'])
def change_note_request():
    note_id = request.values['note_id']
    note_name = request.values['note_name']

    session['note_id'] = note_id
    session['note_name'] = note_name

    return redirect(url_for('root'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
