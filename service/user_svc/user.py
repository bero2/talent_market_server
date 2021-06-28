from db.user_dao import fetch_user_info, insert_user_info
from flask_bcrypt import generate_password_hash
from models.user import User
from typing import *


def register_user(
        db_conf: Mapping[str, str],
        user_id: str,
        user_nm: str,
        user_pw: str,
        user_email: int,
        phone_number: str,
        user_auth: str
):
    exist_user: Optional[User] = fetch_user_info(db_conf, user_id)

    if exist_user is None:
        if user_email == exist_user.user_email:
            return {
                'code': 'DUPLICATED_EMAIL',
                'message': '해당 이메일을 사용하실 수 없습니다'
            }
        else:
            user = User(
                user_id=user_id,
                user_nm=user_nm,
                user_pw_hash=generate_password_hash(user_pw).decode('utf-8'),
                user_email=user_email,
                phone_number=phone_number,
                user_auth=user_auth
            )
        try:
            insert_user_info(db_conf, user)
            return {
                'code': 'SUCCESS_USER_REGISTER',
                'message': '사용자 등록이 완료되었습니다'
            }
        except Exception as e:
            return {
                    'code': 'FAIL_USER_REGISTER',
                    'message': '사용자 등록에 실패했습니다'
                }
    else:
        return {
            'code': 'EXIST_USER',
            'message': '이미 존재하는 사용자입니다'
        }


# TODO 사용자 정보 업데이트
def update_user():
    pass


# TODO 사용자 정보 삭제
def delete_user():
    pass

