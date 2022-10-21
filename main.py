from crypt import methods
import flask
import birthday
from datetime import datetime

app = flask.Flask(__name__)

birthday_manager = birthday.BirthdayManager()

@app.route('/')
@app.route('/index.html')
def root():
    # root template will render index.html
    birthdays = birthday_manager.get_birthdays_html()
    today = datetime.strftime(datetime.today(), '%b %d, %Y')
    return flask.render_template('index.html', page_title='Birthday Countdown', birthdays=birthdays, today=today)


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
    today = datetime.strftime(datetime.today(), '%b %d, %Y')

    #Only update birthdays if the form was filled completely
    if name and date: 
        formatted_date = datetime.strptime(date,'%Y-%m-%d')
        birthday_manager.create_birthday(name, formatted_date)
    
    birthdays = birthday_manager.get_birthdays_html()

    return flask.render_template('index.html', birthdays=birthdays, name=name, date=date, today=today)
    
        
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
