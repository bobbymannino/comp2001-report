from flask import abort, make_response, request, Headers
import requests
from config import db
from models import Trail, User, trails_schema, trail_schema

AUTH_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def is_user_admin(headers: Headers):
    """Will return True if the user is an admin via the auth API"""

    email = headers.get("x-email")
    password = headers.get("x-password")

    if email is None or password is None:
        return False

    body = {"email": email, "password": password}
    response = requests.post(AUTH_URL, json=body)

    response = response.json()

    return response[1] == 'True'

def read_all():
    trails = Trail.query.all()

    return trails_schema.jsonify(trails)

def read_one(trail_id):
    trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()
    if trail is None:
        abort(404, f"Trail with ID {trail_id} not found")

    return trail_schema.jsonify(trail)

def create():
    if is_user_admin(request.headers) == False:
        abort(401, "Unauthorized credentials")

    trail = request.get_json()

    user = User.query.filter(User.user_id == trail['author_id']).one_or_none()
    if user is None:
        abort(404, f"User with ID {trail['author_id']} not found")

    new_trail = trail_schema.load(trail, session=db.session)
    db.session.add(new_trail)
    db.session.commit()
    return trail_schema.jsonify(new_trail), 201

def update(trail_id):
    if is_user_admin(request.headers) == False:
        abort(401, "Unauthorized credentials")

    existing_trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()

    if existing_trail is None:
        abort(404, f"Trail with ID {trail_id} not found")

    new_trail = request.get_json()
    new_trail['trail_id'] = trail_id

    user = User.query.filter(User.user_id == new_trail['author_id']).one_or_none()
    if user is None:
        abort(404, f"User with ID {new_trail['author_id']} not found")

    new_trail = trail_schema.load(new_trail, session=db.session)

    db.session.merge(new_trail)
    db.session.commit()

    return trail_schema.jsonify(new_trail), 201

def delete(trail_id):
    if is_user_admin(request.headers) == False:
        abort(401, "Unauthorized credentials")

    trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()

    if trail is None:
        abort(404, f"Trail with ID {trail_id} not found")

    db.session.delete(trail)
    db.session.commit()

    return make_response(f"Trail with ID {trail_id} deleted", 200)
