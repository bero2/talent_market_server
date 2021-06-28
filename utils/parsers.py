from typing import *

import pandas as pd
from plum import dispatch

from models.user import User


class ParseUser:
    @dispatch
    def parse_user(self, user: dict):
        return User(
            user['user_id'],
            user['user_nm'],
            user['user_pw'],
            user['user_email'],
            user['phone_number'],
            user['user_auth']
        )

    @dispatch
    def parse_user(self, user: pd.DataFrame):
        user_row = user.iloc[0]

        return User(
            user_row['user_id'],
            user_row['user_nm'],
            user_row['user_pw'],
            user_row['user_email'],
            user_row['phone_number'],
            user_row['user_auth'],
            user_row['use_yn'],
            user_row['del_yn']
        )

    @classmethod
    def parse_users(cls, users: pd.DataFrame) -> Dict[str, User]:
        user_list = list(map(cls._parse_users_from_dataframe, users.iloc))
        return dict(zip(users['user_id'].iloc, user_list))

    @staticmethod
    def _parse_users_from_dataframe(user: pd.DataFrame) -> User:
        return User(
            user['user_id'],
            user['user_nm'],
            user['user_pw'],
            user['user_email'],
            user['phone_number'],
            user['user_auth']
        )
