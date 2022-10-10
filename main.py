import flask

app = flask.Flask(__name__)


@app.route('/')
@app.route('/index.html')
def root():
    # root template will render index.html
    return flask.render_template('index.html', page_title='Birthday Countdown')


@app.route('/about.html')
def about_page():
    return flask.render_template('about.html', page_title='About This Application')


@app.route('/group-info.html')
def group_info_page():
    return flask.render_template('group-info.html', page_title='About This Application')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
