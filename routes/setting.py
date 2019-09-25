from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    Request)

from models.message import Messages
from routes import *

from models.reply import Reply

main = Blueprint('setting', __name__)


@main.route('/')
def index():
    u = current_user()
    board_id = int(request.args.get('board_id', -1))
    return render_template('setting.html', user=u, bid=board_id)


@main.route('/person', methods=['POST'])
def setting_person():
    form = request.form.to_dict()
    u = current_user()
    User.update(u.id, username=form['name'])
    if form['signature'] != '':
        User.update(u.id, signature=form['signature'])
    return redirect(url_for('setting.index'))


@main.route('/password', methods=['POST'])
def setting_password():
    form = request.form.to_dict()
    u = current_user()
    d = dict(
        username=u.username,
        password=form['old_pass'],
    )
    print('setting password', form['new_pass'], form['old_pass'])
    if User.validate_login(d):
        User.update(u.id, password=User.salted_password(form['new_pass']))
        print('change password')
    return redirect(url_for('setting.index'))


@main.route('/header/<int:id>')
def setting_header(id):
    u = current_user()
    User.update(u.id, image='/static/images/headers/{}.jpg'.format(id))

    return redirect(url_for('setting.index'))
