from flask_sqlalchemy import SQLAlchemy
import time

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
    starting_amount = db.Column(db.Integer, nullable=True)
    #  starting amount of medicine
    refills_remaining = db.Column(db.Integer, nullable=True)
    black_box_warning = db.Column(db.String(300), nullable=True)
    dosage = db.Column(db.String(300), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    #ForeignKey connecting prescription and user
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))
    #ForeignKey connecting prescription and doctor
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.schedule_id'))
    #ForeignKey connectiong prescription and schedule
    food = db.Column(db.Boolean, nullable=True)
    #food?
    drink = db.Column(db.Boolean, nullable=True)
    #water?

    #Define a relationship to user
    user = db.relationship("User", backref=db.backref("prescriptions"), order_by=prescription_id)

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.prescription_id'))
    timestamp = db.Column(db.DateTime)
    
    #define  relationship to users
    user = db.relationship("User", backref=db.backref("schedules"), order_by=schedule_id)

    #define a relationship to prescriptions
    prescription = db.relationship("Prescription", backref=db.backref("schedules"), order_by=schedule_id)
    #request.args.getlist from a checklist form. that checklist will contian little boxes
    #list should give backa list of times
    #each item from the checklist is its own row

    def __repr__(self):
        """Provides helpful representation data when printed for debugging purposes."""
        return "<Schedule information: >" % ()


class Doctor(db.Model):
    """Doctor information"""

    __tablename__ = "doctors"

    doctor_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    doctor_name = db.Column(db.String(100), primary_key=True, nullable=False)
    condition = db.Column(db.String(300), nullable=True)
    #for what specific condition does the user see the doctor for?
    phone = db.Column(db.String(20), nullable=True)
    #should I make this phone number a string? or Integer?
    office_address = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        """Provides helpful representation data when printed for debugging purposes."""
        return "<Doctor information: >" % ()

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///medicines'
    #name your database medicines??
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
