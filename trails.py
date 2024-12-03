from flask import abort, make_response, request
import requests
from config import db
from models import Trail, User, trails_schema, trail_schema, user_schema

AUTH_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def is_user_admin(email: str | None, password: str | None):
    """Will return True if the user is an admin via the auth API"""
    if email is None or password is None:
        return False

    body = {"Email": email, "Password": password}
    response = requests.post(AUTH_URL, json=body)

    return response.status_code == 200

def read_all():
    trails = Trail.query.all()

    return trails_schema.jsonify(trails)

def read_one(trail_id):
    trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()
    if trail is None:
        abort(404, f"Trail with ID {trail_id} not found")

    return trail_schema.jsonify(trail)

def create():
    trail = request.get_json()

    user = User.query.filter(User.user_id == trail['author_id']).one_or_none()
    if user is None:
        abort(404, f"User with ID {trail['author_id']} not found")

    new_trail = trail_schema.load(trail, session=db.session)
    db.session.add(new_trail)
    db.session.commit()
    return trail_schema.jsonify(new_trail), 201

def update(trail_id):
    email = request.headers.get("x-email")
    password = request.headers.get("x-password")
    if is_user_admin(email, password) == False:
        abort(401, "Unauthorized credentials")


    trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()

    if trail is None:
        abort(404, f"Trail with ID {trail_id} not found")

    new_trail = trail_schema.load(request.get_json(), session=db.session)
    new_trail.trail_id = trail_id

    db.session.merge(new_trail)
    db.session.commit()

    return trail_schema.jsonify(new_trail), 201

def delete(trail_id):
    email = request.headers.get("x-email")
    password = request.headers.get("x-password")
    if is_user_admin(email, password) == False:
        abort(401, "Unauthorized credentials")

    trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()

    if trail is None:
        abort(404, f"Trail with ID {trail_id} not found")

    db.session.delete(trail)
    db.session.commit()

    return make_response(f"Trail with ID {trail_id} deleted", 200)
