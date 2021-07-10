from flask import Blueprint, request
from flask_login import current_user, login_user, logout_user, login_required

from auth.auth import db_conf, user_loader
from db.user_dao import fetch_user_info

login_bp = Blueprint('login_bp', __name__)


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    request_body = request.get_json(silent=True, force=True)
    user_id = request_body['user_id']
    user_pw = request_body['user_pw']

    if current_user.is_authenticated:
        return {'code': 'ALREADY_LOGGED_IN_USER', 'message': '이미 로그인한 사용자입니다'}

    user = fetch_user_info(db_conf, user_id)
    if user.verify_password(user_pw) is True:
        user = user_loader(user_id)
        print(user)
        if user is None:
            return {'code': 'NOT_REGISTERED_USER', 'message': '등록된 ID가 없습니다'}

        login_user(user, remember=False)
        return {'code': 'SUCCESS_LOGIN', 'message': '로그인에 성공했습니다'}

    return {'code': 'INFORMATION_DOES_NOT_MATCH', 'message': 'ID 또는 비밀번호가 일치하지 않습니다'}


@login_required
@login_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return {'code': "SUCCESS_LOGOUT"}
