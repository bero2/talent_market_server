from flask import Blueprint
from flask_login import login_required

from auth.auth import requires_roles
from models.user import Permission

manager_bp = Blueprint('manager_bp', __name__, url_prefix='/users')


@manager_bp.route('/manager', methods=['GET'])
@login_required
@requires_roles(Permission.MANAGER, Permission.ADMIN)
def manager_page():
    return {'status': 200}

