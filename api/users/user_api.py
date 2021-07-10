from flask import Blueprint
from flask_login import login_required

from auth.auth import requires_roles
from models.user import Permission

user_bp = Blueprint('user_bp', __name__, url_prefix='/users')


@user_bp.route('/user', methods=['GET'])
@login_required
@requires_roles(Permission.USER, Permission.MANAGER, Permission.ADMIN)
def manager_page():
    return {'status': 200}

