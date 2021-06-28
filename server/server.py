import configparser
import os
import pathlib
import site
from functools import wraps
from typing import *

from flask import Flask, request
from flask_login import login_required, current_user, LoginManager, login_user, logout_user
from flask_restful import Api, Resource

from db.user_dao import fetch_all_user_info, fetch_user_info
from utils.parsers import ParseUser
from models.user import Permission

site.addsitedir(str(pathlib.Path(__file__).parent.parent.absolute()))


config = configparser.ConfigParser()
config.read(['./db_conf.ini', '/opt/db_conf.ini'])
db_conf: MutableMapping[str, str] = dict(config['TM'])

server = Flask(__name__)
server.config['JSON_SORT_KEYS'] = False

server.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(server)

api = Api(server)


@login_manager.user_loader
def user_loader(user_id: str) -> Optional[str]:
    df_users = fetch_all_user_info(db_conf)
    users = ParseUser.parse_users(df_users)
    return users.get(user_id)


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.user_auth not in roles:
                return {'code': 'UNAUTHORIZED_USER', 'message': '페이지에 접근할 권한이 없습니다'}
            return f(*args, **kwargs)
        return wrapped
    return wrapper


class Login(Resource):
    def post(self):
        request_body = request.get_json(silent=True, force=True)
        user_id = request_body['user_id']
        user_pw = request_body['user_pw']

        if current_user.is_authenticated:
            return {'code': 'ALREADY_LOGGED_IN_USER', 'message': '이미 로그인한 사용자입니다'}

        user = fetch_user_info(db_conf, user_id)
        if user.verify_password(user_pw) is True:
            user = user_loader(user_id)
            if user is None:
                return {'code': 'NOT_REGISTERED_USER', 'message': '등록된 ID가 없습니다'}

            login_user(user, remember=True)
            return {'code': 'SUCCESS_LOGIN', 'message': '로그인에 성공했습니다'}

        return {'code': 'INFORMATION_DOES_NOT_MATCH', 'message': 'ID 또는 비밀번호가 일치하지 않습니다'}


class Logout(Resource):
    @login_required
    def post(self):
        logout_user()
        return {'CODE': "SUCCESS_LOGOUT"}


class AdminPage(Resource):
    @login_required
    @requires_roles(Permission.ADMIN)
    def get(self):
        return {'status': 200}


class ManagerPage(Resource):
    @login_required
    @requires_roles(Permission.MANAGER)
    def get(self):
        return {'status': 200}


class UserPage(Resource):
    @login_required
    @requires_roles(Permission.USER)
    def get(self):
        return {'status': 200}


api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(AdminPage, '/admin')
api.add_resource(ManagerPage, '/manager')
api.add_resource(UserPage, '/user')


if __name__ == "__main__":
    server.run(host='0.0.0.0', port=3500, debug=True)
