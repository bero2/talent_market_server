from flask import Blueprint
from flask_login import login_required

from auth.auth import requires_roles
from models.user import Permission

register_bp = Blueprint('register_bp', __name__, url_prefix='/product')


@register_bp.route('/register', methods=['GET'])
@login_required
@requires_roles(Permission.MANAGER, Permission.ADMIN)
def register():
    return {'status': 200}


