from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ----------------------------------------
# Model definitions/ skeleton

class User(db.Model):
	"""User of medicine-tracking app. 
	Contains user_id, name and any diagnosed conditions."""

	__tablename__ = "users"

	user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False) 
	name = db.Column(db.String(100), nullable=True)
	condition = db.Column(db.String(150), nullable=True)

	def __repr__(self):
		"""Provides helpful representation data when printed for debugging purposes."""

		return "<User information:>" % ()


class Prescription(db.Model):

	__tablename__ = "prescriptions"

	prescription_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	med_name = db.Column(db.String(200), nullable=False)
	side_effects = db.Column(db.String(200), nullable=True)
	starting_amount = db.Column(db.Integer, nullable=True) #starting amount of medicine
	refills_remaining = db.Column(db.Integer, nullable=True) 
	black_box_warning = db.Column(db.String(300), nullable=True)
	dosage = db.Column(db.String(300), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))#ForeignKey
	doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))#ForeignKey
	schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.schedule_id'))#ForeignKey
	food = db.Column(db.Boolean, nullable=True) #food?
	drink = db.Column(db.Boolean, nullable=True) #water?

	#Define a relationship to user
	user = db.relationship("User",
							backref=db.backref("prescriptions"), order_by=prescription_id)

	#Define a relationship to doctors
	doctor = db.relationship("Doctor", backref=db.backref("prescriptions"), order_by=prescription_id)

	#Define a relationship to schedules
	schedule = db.relationship("Schedule", backref=db.backref("prescriptions"), order_by=prescription_id)
	
	def __repr__(self):
		"""Provides helpful representation data when printed for debugging purposes."""

		return "<Prescription information: >" % ()

class Schedule(db.Model):

	__tablename__ = "schedules"

	schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

	# date_started = db.Column(pass) #??look up datetime object stuff
	# date_time = db.Column(pass) #??  must convert to datetime object
	#HALP ???------------------


	def __repr__(self):
		"""Provides helpful representation data when printed for debugging purposes."""

		return "<Schedule information: >" % ()

class Doctor(db.Model):
	"""Doctor information"""

	__tablename____ = "doctors"

	doctor_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
	doctor_name = db.Column(db.String(100), primary_key=True, nullable=False) 
	condition = db.Column(db.String(300), nullable=True) #for what specific condition does the user see the doctor for? 
	phone = db.Column(db.String(20), nullable=True) #should I make this phone number a string? or Integer?
	office_address = db.Column(db.String(200), nullable=True)

	def __repr__(self):
		"""Provides helpful representation data when printed for debugging purposes."""

		return "<Doctor information: >" % ()