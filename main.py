from crypt import methods
import flask
import birthday
import datetime

app = flask.Flask(__name__)

birthday_manager = birthday.BirthdayManager()

@app.route('/')
@app.route('/index.html')
def root():
    # root template will render index.html
    birthdays = birthday_manager.get_birthdays_html()
    return flask.render_template('index.html', page_title='Birthday Countdown', birthdays=birthdays)


@app.route('/about.html')
def about_page():
    return flask.render_template('about.html', page_title='About This Application')


@app.route('/group-info.html')
def group_info_page():
    return flask.render_template('group-info.html', page_title='About This Application')

@app.route('/push', methods=['POST', 'GET'])
def push_birthday():
    name = flask.request.form['name']
    date = datetime.datetime.strptime(flask.request.form['date'],'%Y-%m-%d')
    if name and date: 
        birthday_manager.create_birthday(name, date)

    birthday_manager.clear_birthdays()
    birthdays = birthday_manager.get_birthdays_html()

    return flask.render_template('index.html', birthdays=birthdays, name=name, date=date)
        


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
