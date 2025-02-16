# app/routes/api.py

from flask import Blueprint
from app.controllers.hive_controller import hive_blueprint

api_bp = Blueprint('api_bp', __name__)

# Register the hive blueprint under /api/hives
api_bp.register_blueprint(hive_blueprint, url_prefix='')
