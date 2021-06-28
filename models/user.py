from flask_bcrypt import check_password_hash


class Permission:
    GUEST = 1
    USER = 2
    MANAGER = 3
    ADMIN = 4


class User:
    def __init__(
            self,
            user_id: str,
            user_nm: str,
            user_pw_hash: str,
            user_email: int,
            phone_number: str,
            user_auth: str,
            use_yn: str = 'Y',
            del_yn: str = 'N',
            authenticated: bool = False
    ):
        self.user_id = user_id
        self.user_nm = user_nm
        self.user_pw_hash = user_pw_hash
        self.user_email = user_email
        self.phone_number = phone_number
        self.user_auth = int(user_auth)
        self.use_yn = use_yn
        self.del_yn = del_yn
        self.authenticated = authenticated

    def verify_password(self, password):
        return check_password_hash(self.user_pw_hash, password)

    def is_admin(self):
        return self.user_auth == Permission.ADMIN

    def is_manager(self):
        return self.user_auth == Permission.MANAGER

    def is_user(self):
        return self.user_auth == Permission.USER

    def is_guest(self):
        return self.user_auth == Permission.GUEST

    def allowed(self, auth_level):
        return self.user_auth >= auth_level

    def can_login(self, passwd_hash):
        return self.user_pw_hash == passwd_hash

    @property
    def is_active(self):
        return True

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return self.authenticated

    @property
    def is_anonymous(self):
        return False

    def __repr__(self) -> str:
        r = {
            'user_id': self.user_id,
            'email': self.user_email,
            'passwd_hash': self.user_pw_hash,
            'authenticated': self.authenticated,
        }
        return str(r)

