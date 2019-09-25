import uuid
from functools import wraps

import json
import redis
from flask import session, request, abort

from models.user import User
from utils import log


# def current_user():
#     if 'session_id' in request.cookies:
#         session_id = request.cookies['session_id']
#         s = Session.one_for_session_id(session_id=session_id)
#         key = 'session_id_{}'.format(session_id)
#         user_id = int(cache.get(key))
#         log('current_user key <{}> user_id <{}>'.format(key, user_id))
#         u = User.one(id=user_id)
#         return u
#     else:
#         return None

def current_user():
    uid = session.get('user_id', '')
    u: User = User.one(id=uid)
    # type annotation
    # User u = User.one(id=uid)
    return u


cache = redis.StrictRedis()
# csrf_tokens = dict()


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        k = 'csrf_token_{}'.format(token)

        if cache.exists(k):
            v = cache.get(k)
            user_id = json.loads(v)
            if user_id == u.id:
                cache.delete(token)
                return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    k = 'csrf_token_{}'.format(token)
    v = json.dumps(u.id)
    cache.set(k, v)
    return token
