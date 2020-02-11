from datetime import datetime
from image_repo import db

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Image number {self.id}"