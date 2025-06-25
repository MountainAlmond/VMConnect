from models.engine import db

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))
    routes = db.Column(db.JSON, nullable=False, default=[])  # Список маршрутов в формате JSON