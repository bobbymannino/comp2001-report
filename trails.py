from marshmallow import EXCLUDE
from flask import abort, make_response, request, Request
import requests
from config import db
from models import Trail, TrailSchema, User, Point, PointSchema, TrailPoint, TrailPointSchema
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

def get_point(trail_point):
    point = Point.query.filter(Point.point_id == trail_point.point_id).one_or_none()
    if point is None:
        return None

    return {
        "position": trail_point.position,
        "longitude": point.longitude,
        "latitude": point.latitude,
        "description": point.description
    }

def read_one(trail_id):
    trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()
    if trail is None:
        abort(404, f"Trail with ID {trail_id} not found")

    points = map(get_point, trail.trail_points)
    points = list(filter(None, points))

    trail = TrailSchema().dump(trail);

    return json.loads(json.dumps(trail)) | {"points": points}

def create():
    if is_user_admin(request) == False:
        abort(401, "Unauthorized credentials")

    trail = request.get_json()

    email = request.headers.get("x-email")
    user = User.query.filter(User.email == email).one_or_none()
    if user is None:
        abort(404, f"User with email {email} not found")

    # check if user is admin
    if user.role != 'ADMIN':
        abort(401, "Not an admin")

    points = trail['points']
    trail = {
        "author_id": user.user_id,
        "name": trail['name'],
        "summary": trail['summary'],
        "description": trail['description'],
        "location": trail['location'],
        "length": trail['length'],
        "elevation_gain": trail['elevation_gain'],
        "route_type": trail['route_type']
    }
    new_trail = TrailSchema().load(trail, session=db.session)
    db.session.add(new_trail)
    db.session.commit()

    # add points to trail_points
    for point in points:
        p = {
            "longitude": point['longitude'],
            "latitude": point['latitude'],
            "description": point['description']
        }
        new_point = PointSchema().load(p, session=db.session)
        db.session.add(new_point)
        db.session.commit()

        p = {
            "trail_id": new_trail.trail_id,
            "point_id": new_point.point_id,
            "position": point['position']
        }
        new_trail_point = TrailPointSchema().load(p, session=db.session)
        db.session.add(new_trail_point)

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
