import os

from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()


def create_app():
    app = Flask(__name__, instance_relative_config=False)

    login_manager.init_app(app)

    app.config['JSON_SORT_KEYS'] = False
    app.secret_key = os.urandom(24)

    with app.app_context():
        from api.login import login_api
        from api.users import admin_api
        from api.users import manager_api
        from api.users import user_api
        from api.product import regist_api

        app.register_blueprint(login_api.login_bp)
        app.register_blueprint(admin_api.admin_bp)
        app.register_blueprint(manager_api.manager_bp)
        app.register_blueprint(user_api.user_bp)
        app.register_blueprint(regist_api.register_bp)

        return app
