from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ----------------------------------------
# Model definitions/ skeleton

class User(db.Model):
	"""User of medicine-tracking app. 
	Contains id, name and any diagnosed conditions."""

	__tablename__ = "users"

	id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	name = db.Column(db.String(100), nullable=True)
	condition = db.Column(db.String(150), nullable=True)

	def __repr__(self):
		"""Provides helpful representation data when printed for debugging purposes."""

		return "<User information: id=%s name=%s condition=%s>" %(self.id, self.name, self.condition)
