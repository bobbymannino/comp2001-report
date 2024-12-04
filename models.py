from config import db, ma
from marshmallow_sqlalchemy import fields

class TrailPoint(db.Model):
    __tablename__ = "trail_points"
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    trail_id = db.Column(db.Integer, db.ForeignKey("CW2.trails.trail_id"), primary_key=True)
    point_id = db.Column(db.Integer, db.ForeignKey("CW2.points.point_id"), primary_key=True)
    position = db.Column(db.Integer)

class TrailPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrailPoint
        load_instance = True
        sql_session = db.session
        include_fk = True

class Point(db.Model):
    __tablename__ = "points"
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    point_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    description = db.Column(db.Text)

    trail_points = db.relationship('TrailPoint', backref='trail_point')


class PointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Point
        load_instance = True
        sql_session = db.session
        include_relationships = True

    trail_points = fields.Nested(TrailPointSchema, many=True)

class Trail(db.Model):
    __tablename__ = "trails"
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    trail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    summary = db.Column(db.Text)
    description = db.Column(db.Text)
    location = db.Column(db.Text)
    route_type = db.Column(db.Text)
    length = db.Column(db.Integer)
    elevation_gain = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey("CW2.users.user_id"))
    points = db.relationship('Point', backref='point')

    trail_points = db.relationship('TrailPoint', backref='trail_point')

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sql_session = db.session
        include_fk = True
        include_relationships = True

    points = fields.Nested(PointSchema, many=True)

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'schema': 'CW2', 'extend_existing': True}

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text)
    role = db.Column(db.Text)

    trails = db.relationship(
        Trail,
        backref="trail",
        single_parent=True,
        order_by="desc(Trail.name)"
    )

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sql_session = db.session
        include_relationships = True

    trails = fields.Nested(TrailSchema, many=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)

point_schema = PointSchema()
points_schema = PointSchema(many=True)

trail_point_schema = TrailPointSchema()
trail_points_schema = TrailPointSchema(many=True)
