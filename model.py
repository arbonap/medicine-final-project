from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ----------------------------------------
# Model definitions/ skeleton

class User(db.Model):
	"""User of medicine-tracking app. 
	Contains user_id, name and any diagnosed conditions."""

	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True, nullable=False) #connect this to prescription
	name = db.Column(db.String(100), nullable=True)
	condition = db.Column(db.String(150), nullable=True)

	def __repr__(self):
		"""Provides helpful representation data when printed for debugging purposes."""

		return "<User information:>" % ()


class Prescription(db.Model):

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	med_name = db.Column(db.String(200), nullable=False)
	side_effects = db.Column(db.String(200), nullable=True) #I need to make a new table for side_effects
	starting_amount = db.Column(db.Integer, nullable=True) #starting amount of medicine
	refills_remaining = db.Column(db.Integer, nullable=True) #is there a way to autodecrement? must have a starting # of refills though..
	black_box_warning = db.Column(db.String(300), nullable=True)
	dosage = db.Column(db.String(300), nullable=False)
	#include foreign key user id

	def __repr__(self):
		"""Provides helpful representation data when printed for debugging purposes."""

		return "<Prescription information: >" % ()

class Schedule(db.Model):

	id = db.Column(db.Integer, primary_key=True, nullable=False)
	prescription_id = db.Column(db.string(200), nullable=False) #Foreign key !!connect to id in Prescription class
	date_started = db.Column(pass) #??
	date_time = db.Column(pass) #??  must convert to datetime object
	food_water = db.Column(db.Boolean(200), nullable=True) #food and or water requirements: find boolean


	def __repr__(self):
		"""Provides helpful representation data when printed for debugging purposes."""

		return "<Schedule information: >" % ()

class SideEffects(db.Model):

	id = db.Column(db.Integer, primary_key=True, nullable=False)



# class Doctor(db.Model):
# 	"""Doctor information"""

# 	__tablename____ = "doctors"

# 	doctor_name = db.Column(db.String(100), primary_key=True, nullable=False) #not unique because I technically can have doctors with the same name?
# 	specialty = db.Column(db.String(100), nullable=True)
# 	condition = db.Column(db.String(300), nullable=True) #for what specific condition does the user see the doctor for? #foreignKey perhaps?
# 	gender = db.Column(db.String(50), nullable=True)
# 	age = db.Column(db.Integer, nullable=True)
# 	board_certification = db.Column(db.Boolean) #is this correct for making Boolean values?
# 	hospital_affiliation = db.Column(db.String(250), nullable=True)
# 	private_practice_affiliation = db.Column(db.String(250), nullable=True)
# 	phone = db.Column(db.String(20), nullable=True) #should I make this phone number a string? or Integer?
# 	office_address = db.Column(db.String(200), nullable=True)

	# def __repr__(self):
	# 	"""Provides helpful representation data when printed for debugging purposes."""

	# 	return "<Doctor information: >" % (self.doctor_name, self.specialty, self.phone, self.office_address)