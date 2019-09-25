import datetime

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    Request)

from routes import *

from models.reply import Reply
from models.topic import Topic
from models.user import User

main = Blueprint('person', __name__)


@main.route('/')
def index():
    u = current_user()
    if u is None:
        abort(404)
    else:
        return redirect(url_for('.user_home', name=u.username))


@main.route('/<int:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        return redirect(url_for('.user_home', name=u.username))


@main.route('/<string:name>')
def user_home(name):
    u = User.one(username=name)
    date = datetime.datetime.fromtimestamp(u.created_time)

    replies = Reply.all(user_id=u.id)
    launch_topic = Topic.all(user_id=u.id)
    replies.sort(key=lambda t: t.created_time, reverse=True)
    launch_topic.sort(key=lambda t: t.created_time, reverse=True)

    join_topic = []
    for reply in replies:
        topic = Topic.one(id=reply.topic_id)
        if [reply, topic.title] not in join_topic:
            join_topic.append([reply, topic.title])
    if u is None:
        abort(404)
    else:
        return render_template('user.html', user=u, launch=launch_topic, join=join_topic, time=date)
