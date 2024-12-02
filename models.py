from config import db, ma
from marshmallow_sqlalchemy import fields


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

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sql_session = db.session
        include_fk = True

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'schema': 'CW2'}

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

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
