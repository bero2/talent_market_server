from flask import Blueprint
from flask_login import login_required

from auth.auth import requires_roles
from models.user import Permission

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/users')


@admin_bp.route('/admin', methods=['GET'])
@login_required
@requires_roles(Permission.ADMIN)
def admin_page():
    return {'status': 200}


