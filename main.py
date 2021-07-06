import unittest
from flask import request, flash, make_response, redirect, render_template, session, url_for
from flask_login import login_required, current_user

from app import create_app
from app.forms import LoginForm
from app.firestore_service import get_users, get_todos

app = create_app()


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def not_found(error):
    return render_template('500.html', error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))

    session['user_ip'] = user_ip
    return response


@app.route('/hello', methods=['GET'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username
    }
    # users = get_users()
    #
    # for user in users:
    #     print(user.id)
    #     print(user.to_dict()['password'])
    # return 'Hellos World Platzi, tu IP es: {}'.format(user_ip)
    return render_template('hello.html', **context)
