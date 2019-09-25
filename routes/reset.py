from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from config import admin_mail
from models.message import send_mail
from routes import *

main = Blueprint('reset', __name__)

ip = '49.235.24.224'
user_tokens = dict()


@main.route('/send', methods=['POST'])
def reset_send():
    form = request.form.to_dict()
    u = User.one(username=form['username'])
    if u is not None:
        token = str(uuid.uuid4())
        k = 'reset_token_{}'.format(token)
        v = json.dumps(u.id)
        cache.set(k, v)
        send_mail(
            subject='Reset your password',
            author=admin_mail,
            to=u.email,
            content='http://{}/reset/view?token={}'.format(ip, token),
        )
    return redirect(url_for('index.index'))


@main.route('/view')
def reset_view():
    args = request.args
    token = args.get('token', None)
    if token is None:
        return redirect(url_for('index.index'))
    else:
        return render_template('resetPassword.html', token=token)


@main.route('/update', methods=['POST'])
def reset_update():
    form = request.form.to_dict()
    token = form.get('resetToken', None)
    k = 'reset_token_{}'.format(token)

    if cache.exists(k):
        v = cache.get(k)
        user_id = json.loads(v)

        User.update(user_id, password=User.salted_password(form['password']))

    return redirect(url_for('index.index'))
