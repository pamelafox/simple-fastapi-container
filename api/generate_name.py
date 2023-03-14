import random

from flask import Blueprint, jsonify, request

from .data import names

bp = Blueprint("names", __name__)


@bp.route("/generate_name")
def generate_name():
    starts_with = request.args.get("starts_with")
    name_choices = names
    if starts_with:
        name_choices = [name for name in names if name.lower().startswith(starts_with.lower())]
    random_name = random.choice(name_choices)
    result = {"name": random_name}
    return jsonify(result)
