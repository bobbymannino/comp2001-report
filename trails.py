from flask import abort, make_response, request

from config import db
from models import Trail, trails_schema, trail_schema

def read_all():
    trails = Trail.query.all()

    return trails_schema.jsonify(trails)

def read_one(trail_id):
    trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()

    if trail is not None:
        return trail_schema.jsonify(trail)
    else:
        abort(404, f"Trail with ID {trail_id} not found")

def create(trail):
    print("Hi")
    # lname = person.get("lname")
    #     existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    #     if existing_person is None:
    #         new_person = person_schema.load(person, session=db.session)
    #         db.session.add(new_person)
    #         db.session.commit()
    #         return person_schema.dump(new_person), 201
    #     else:
    #         abort(406, f"Person with last name {lname} already exists")

def update(trail_id, trail):
    print("Hi")
    # existing_person = Person.query.filter(Person.lname == lname).one_or_none()

    # if existing_person:
    #     update_person = person_schema.load(person, session=db.session)
    #     existing_person.fname = update_person.fname
    #     db.session.merge(existing_person)
    #     db.session.commit()
    #     return person_schema.dump(existing_person), 201
    # else:
    #     abort(404, f"Person with last name {lname} not found")

def delete(trail_id):
    email = request.headers.get("x-email")
    password = request.headers.get("x-password")

    trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()

    if trail is not None:
        # db.session.delete(trail)
        # db.session.commit()
        return make_response(f"Trail with ID {trail_id} deleted", 200)
    else:
        abort(404, f"Trail with ID {trail_id} not found")
