from config import db, ma
from marshmallow_sqlalchemy import fields
from marshmallow import fields

class TrailPoint(db.Model):
    __tablename__ = "trail_points"
    __table_args__ = {'schema': 'CW2', "extend_existing": True}

    trail_id = db.Column(db.Integer, db.ForeignKey("CW2.trails.trail_id"), primary_key=True)
    point_id = db.Column(db.Integer, db.ForeignKey("CW2.points.point_id"), primary_key=True)
    position = db.Column(db.Integer, nullable=False)

class TrailPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailPoint
        load_instance = True
        sqla_session = db.session

    trail_id = fields.Integer(required=True)
    point_id = fields.Integer(required=True)

class Trail(db.Model):
    __tablename__ = "trails"
    __table_args__ = {'schema': 'CW2', "extend_existing": True}

    trail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    length = db.Column(db.Integer, nullable=False)
    elevation_gain = db.Column(db.Integer, nullable=False)
    route_type = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("CW2.users.user_id"), nullable=False)

    trail_points = db.relationship(TrailPoint, backref="trail_trail_points", single_parent=True)

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session

    author_id = fields.Integer(required=True)

class Point(db.Model):
    __tablename__ = "points"
    __table_args__ = {'schema': 'CW2', "extend_existing": True}

    point_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)

    trail_points = db.relationship(TrailPoint, backref="point_trail_points", single_parent=True)

class PointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Point
        load_instance = True
        sqla_session = db.session

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'schema': 'CW2', "extend_existing": True}

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    role = db.Column(db.Text, nullable=False)

    trails = db.relationship(Trail, backref="author", single_parent=True)
