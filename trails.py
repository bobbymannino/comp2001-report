from flask import abort, make_response

from config import db
from models import Trail, trails_schema, trail_schema

def read_all():
    trails = Trail.query.all()
    return trails_schema.jsonify(trails)

def read_one(trailId):
    trail = Trail.query.filter(Trail.trail_id == trailId).one_or_none()

    if trail is not None:
        return trail_schema.jsonify(trail)
    else:
        abort(404, f"Trail with ID {trailId} not found")

def create(trail):
    print("CREATE")

def update(id, trail):
    print("UPDAET")

def delete(id):
    print("DELETE")
