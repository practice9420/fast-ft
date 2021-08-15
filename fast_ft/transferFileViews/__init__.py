from flask import Blueprint

transfer = Blueprint('transferFile', __name__)

from . import transferViews, chartViews
