import configparser
from functools import wraps
from typing import *

from flask_login import current_user

from db.user_dao import fetch_all_user_info
from server import login_manager
from utils.parsers import ParseUser

config = configparser.ConfigParser()
config.read(['./db_conf.ini', '/opt/db_conf.ini'])
db_conf: MutableMapping[str, str] = dict(config['TM'])


@login_manager.user_loader
def user_loader(user_id: str) -> Optional[str]:
    df_users = fetch_all_user_info(db_conf)
    users = ParseUser.parse_users(df_users)
    print(users)
    return users.get(user_id)


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            print(roles, current_user.user_auth)
            if current_user.user_auth not in roles:
                return {'code': 'UNAUTHORIZED_USER', 'message': '페이지에 접근할 권한이 없습니다'}
            return f(*args, **kwargs)
        return wrapped
    return wrapper
