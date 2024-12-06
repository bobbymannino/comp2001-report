from flask import abort, make_response, request, Request
import requests
from config import db
from models import Trail, TrailSchema, User, Point
import json

AUTH_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def is_user_admin(req: Request):
    """Will return True if the user is an admin via the auth API"""

    email = req.headers.get("x-email")
    password = req.headers.get("x-password")

    if email is None or password is None:
        return False

    body = {"email": email, "password": password}
    response = requests.post(AUTH_URL, json=body)

    response = response.json()

    return response[1] == 'True'

def read_all():
    trails = Trail.query.all()

    return TrailSchema(many=True).dump(trails)

def m(x):
    point = Point.query.filter(Point.point_id == x.point_id).one_or_none()
    if point is None:
        return None

    return {
        "position": x.position,
        "longitude": point.longitude,
        "latitude": point.latitude,
        "description": point.description
    }


def read_one(trail_id):
    trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()
    if trail is None:
        abort(404, f"Trail with ID {trail_id} not found")

    points = map(m, trail.trail_points)
    points = list(filter(None, points))

    trail = TrailSchema().dump(trail);

    return json.loads(json.dumps(trail)) | {"points": points}

def create():
    if is_user_admin(request) == False:
        abort(401, "Unauthorized credentials")

    trail = request.get_json()

    # add points to trail_points

    user = User.query.filter(User.user_id == trail['author_id']).one_or_none()
    if user is None:
        abort(404, f"User with ID {trail['author_id']} not found")

    new_trail = TrailSchema().load(trail, session=db.session)
    db.session.add(new_trail)
    db.session.commit()
    return TrailSchema().dump(new_trail), 201

def update(trail_id):
    if is_user_admin(request) == False:
        abort(401, "Unauthorized credentials")

    existing_trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()

    if existing_trail is None:
        abort(404, f"Trail with ID {trail_id} not found")

    new_trail = request.get_json()
    new_trail['trail_id'] = trail_id

    user = User.query.filter(User.user_id == new_trail['author_id']).one_or_none()
    if user is None:
        abort(404, f"User with ID {new_trail['author_id']} not found")

    new_trail = TrailSchema().load(new_trail, session=db.session)

    db.session.merge(new_trail)
    db.session.commit()

    return TrailSchema().dump(new_trail), 201

def delete(trail_id):
    if is_user_admin(request) == False:
        abort(401, "Unauthorized credentials")

    trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()

    if trail is None:
        abort(404, f"Trail with ID {trail_id} not found")

    for point in trail.trail_points:
        db.session.delete(point)

    db.session.delete(trail)
    db.session.commit()

    return make_response(f"Trail with ID {trail_id} deleted", 200)
