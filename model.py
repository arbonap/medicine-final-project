from flask_sqlalchemy import SQLAlchemy
import time

db = SQLAlchemy()

# ----------------------------------------
# Model definitions/ skeleton


class User(db.Model):
    """User of medicine-tracking app.
    Contains user_id, name and ."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                        nullable=False)
    phone = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provides helpful representation data when printed for debugging purposes."""

        return "<User ID user_id=%s phone phone=%s password password=%s  \
                email email=%s first_name first_name=%s \
                last_name last_name=%s>" % (self.user_id, self.phone,
                                            self.password, self.email,
                                            self.first_name, self.last_name)


class Prescription(db.Model):

    __tablename__ = "prescriptions"

    prescription_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                                nullable=False)
    reason = db.Column(db.String(150), nullable=True)
    med_name = db.Column(db.String(200), nullable=False)
    side_effects = db.Column(db.String(200), nullable=True)
    starting_amount = db.Column(db.Integer, nullable=True)
    #  starting amount of medicine
    refills_remaining = db.Column(db.Integer, nullable=True)
    black_box_warning = db.Column(db.String(300), nullable=True)
    dosage_quantity = db.Column(db.Integer, nullable=False)
    dosage_timing = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    food = db.Column(db.Boolean, nullable=True)
    #food?
    drink = db.Column(db.Boolean, nullable=True)
    #water?
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    #ForeignKey connecting prescription and user
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))
    #ForeignKey connecting prescription and doctor
    # schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.schedule_id'))
    #ForeignKey connection: prescription and schedule

    #Define a relationship to user
    user = db.relationship("User", backref=db.backref("prescriptions"),
                           order_by=prescription_id)

    #Define a relationship to doctors
    doctor = db.relationship("Doctor", backref=db.backref("prescriptions"),
                             order_by=prescription_id)

    #Define a relationship to schedules
    # schedule = db.relationship("Schedule",
    #                            backref=db.backref("prescriptions"),
    #                            order_by=prescription_id)

    def __repr__(self):
        """Provides helpful representation data when printed for debugging purposes."""

        return "<Prescription id prescription_id=%s med_name med_name=%s>" % (self.prescription_id, self.med_name)


class Schedule(db.Model):

    __tablename__ = "schedules"

    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                            nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.prescription_id'), nullable=False)
    timestamp = db.Column(db.Time, nullable=False)

    def __repr__(self):
        """Provides helpful representation data when printed for debugging purposes."""
        return "<Schedule_id schedule_id=%s timestamp timestamp=%s>" % (self.schedule_id, self.timestamp)


class Doctor(db.Model):
    """Doctor information"""

    __tablename__ = "doctors"

    doctor_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    doctor_name = db.Column(db.String(100), nullable=False)
    condition = db.Column(db.String(300), nullable=True)
    #for what specific condition does the user see the doctor for?
    phone = db.Column(db.String(20), nullable=True)
    #should I make this phone number a string? or Integer?
    office_address = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        """Provides helpful representation data when printed for debugging purposes."""
        return "<doctor_id doctor_id=%s doctor_name doctor_name=%s \
                condition condition=%s phone phone=%s \
                office_address=%s>" % (self.doctor_id,
                                       self.doctor_name,
                                       self.condition,
                                       self.phone,
                                       self.office_address)


# class Dosage_time(db.Model):
#     """Timing for when user takes medication"""

#     ___tablename___ = "dosage_times"

#     time_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
#     timestamp = db.Column(db.Time, nullable=True)
#     # TODO: CHANGE DOSAGE_ID TO PRESCRIPTION_ID, HERE AND LINE 188 ON SERVER.PY
#     dosage_id = db.Column(db.Integer, db.ForeignKey('prescriptions.prescription_id'))
#     # define a relationship to prescriptions
#     prescriptions = db.relationship("Prescription", backref=db.backref("dosage_times"),
#                                     order_by=dosage_id)
# know what exactly dosage_id and prescriptions are relating to
# comprehend the one to one and one to many relationships in your model

#     def __repr__(self):
#         """Provides helpful representation data when printed for debugging purposes."""

#         return "<Time id time_id=%s Timestamp  timestamp=%s>" % (self.time_id, self.timestamp)

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///medicines'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
