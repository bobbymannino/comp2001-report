from config import db, ma

class Trail(db.Model):
    __tablename__ = "trails"
    trail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    length = db.Column(db.Integer)

    __table_args__ = {'schema': 'CW2'}

class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sql_session = db.session

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)
