from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Prescription, Schedule, Doctor
from datetime import datetime, timedelta
# from datetime the module, you're importing datetime the class (both are called datetime)
# static methods are called directly from the class

app = Flask(__name__)

# app.config.update(
#     DEBUG=True,
#     #EMAIL SETTINGS
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT=465,
#     MAIL_USE_SSL=True,
#     MAIL_USERNAME=os.environ['GMAIL_USER_NAME'],
#     MAIL_PASSWORD=os.environ['GMAIL_PASSWORD']
#     )

# mail = Mail(app)

# app.secret_key = os.environ['FLASK_KEY']
# app.jinja_env.undefined = StrictUndefined

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
#???

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is so Jinja2 doesn't fail silently and gives an error
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    user_id = session.get("user_id")

    email = session.get("email")

    reminder(user_id)

    if user_id:
        flash("You are currently logged in as %s " % email)
    else:
        flash("You are not logged in as anyone")
    # person_id is the argument
    return render_template("homepage.html")


@app.route('/sign-up', methods=['GET'])
def sign_up_form():
    """Show form for user signup."""

    return render_template("sign-up.html")


@app.route('/sign-up', methods=['POST'])
def sign_up_process():
    """Sign-up process registration."""

     # get form variables
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    email = request.form["email"]
    password = request.form["password"]
    phone_number = request.form["phone_number"]

    new_user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    phone=phone_number)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)

    return redirect('/')
    #is this correct?


@app.route('/login')
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/loggedin', methods=['POST'])
def login_user():
    """Process log-in"""

    # Get form variables
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    # print user.email

    if not user:
        flash("Drat! No such user or incorrect username.")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password, try again.")
        return redirect("/login")

    session["user_id"] = user.user_id
    session['email'] = user.email
    session['first_name'] = user.first_name
    # # is this correct? not sure

    flash("Logged in as %s" % email)
    return redirect("/")
    # where to direct this page?


@app.route('/logout', methods=['GET'])
def logout():
    """Log out."""

    # del session["user_id"]
    # del session["email"]
    # del session["first_name"]
    session.clear()
    flash("User Logged out...Goodbye!")
    return redirect("/")


@app.route('/register', methods=['GET'])
def register():
    """Sends user to fill out medicine information"""
    #Get form variables
    logged_in_user_id = session.get("user_id")
    logged_in_user_email = session.get("email")
    if logged_in_user_id:
        flash("You are currently logged in as %s " % logged_in_user_email)
    else:
        flash("You are not logged in as anyone")

    return render_template("register.html")


@app.route('/medication', methods=['POST'])
def submittal():
    """Getting variables from medication registeration form"""
    logged_in_user_id = session.get("user_id")
    print logged_in_user_id
    logged_in_user_email = session.get("email")
    print logged_in_user_email

    if logged_in_user_id:
        reason = request.form.get("reason")
        med_name = request.form.get("med_name")
        side_effects = request.form.get("side_effects")
        starting_amount = int(request.form.get("starting_amount"))
        #starting amount is an integer
        refills_remaining = int(request.form.get("refills_remaining"))
        #refills remaining is an integer
        black_box_warning = request.form.get("black_box_warning")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        dosage_timing = int(request.form.get("dosage_timing"))
        dosage_quantity = int(request.form.get("dosage_quantity"))
        #dosage is a string so no need for an integer
        food = bool(request.form.get("food"))
        water_boolean = bool(request.form.get("water"))
        daily_schedule = request.form.getlist("daily_schedule")

        print water_boolean
        print food
        print start_date
        print daily_schedule
        print "LOOK AT ME HERE!!!!!!!!!!! ABOVE IS DAILY SCHEDULE TIME!!!!!!!!!!"

        new_prescription = Prescription(user_id=logged_in_user_id,
                                        reason=reason,
                                        med_name=med_name,
                                        side_effects=side_effects,
                                        starting_amount=starting_amount,
                                        refills_remaining=refills_remaining,
                                        black_box_warning=black_box_warning,
                                        start_date=start_date,
                                        end_date=end_date,
                                        dosage_timing=dosage_timing,
                                        dosage_quantity=dosage_quantity,
                                        food=food,
                                        drink=water_boolean,
                                        )
        db.session.add(new_prescription)
        db.session.commit()

        new_prescription_id = Prescription.query.filter_by(user_id=logged_in_user_id,
                                                           med_name=med_name,
                                                           start_date=start_date).first()

        print new_prescription_id

        for time_string in daily_schedule:
            print time_string
        #   1.first convert time string into datetime object that's just the time in HOUR:MINUTE:SECONDS format
            timestamp = datetime.strptime(time_string, "%H:%M:%S")
            print timestamp
        #   2. make dosage time object:
        #  ???????????????????????? uh
            new_dosage_time = Schedule(user_id=logged_in_user_id,
                                       timestamp=timestamp,
                                       prescription_id=new_prescription_id.user_id)
            print new_dosage_time
        #   3. do db.add -  #
            db.session.add(new_dosage_time)
            db.session.commit()

        flash("Medication %s added." % med_name)
        flash("You are logged in as %s" % logged_in_user_email)
        return redirect("/")
    else:
        flash("User is not logged in.")
        return redirect("/login")


@app.route('/show_meds', methods=["GET"])
def show_meds():
    """Shows the meds the user currently takes"""
    # print sqlalchemy queries here
    logged_in_user_id = session.get("user_id")
    if logged_in_user_id:
        all_meds = Prescription.query.filter_by(user_id=logged_in_user_id).all()

        #must be .first() rather than .one() because .one() expects ATLEAST one and only one object
        # while .first() will throw an error
        user = User.query.filter_by(user_id=logged_in_user_id).first()

        # datetime.strptime(input_datetime, "%b-%d-%Y-%I-%M")
        rx_timestamp = Schedule.query.filter_by(user_id=logged_in_user_id).all()

        print rx_timestamp
        # this dictionary is necessary in order for jinja to later loop over (because jinja can only do simple for loops)
        pres_names = {}
        for pres in all_meds:
            pres_names[pres.prescription_id] = [pres.med_name]
        print pres_names
        print "!!!!ABOVE IS PRES_NAMES!!!"
        # print pres_names should output something like:
        # {1: [u'example']}

        # this dictionary is necessary in order for jinja to later loop over (because jinja can only do simple for loops)
        # pres_times = {}
        # for time in rx_timestamp:
        #     if time.prescription_id in pres_times:
        #         pres_times[time.prescription_id].append(time.timestamp.strftime("%H:%M:%S"))
        #     else:
        #         pres_times[time.prescription_id] = [time.timestamp.strftime("%H:%M:%S")]

        # print pres_times
        # print "ABOVE IS PRES_TIMES!!!!!!!!!!!!!"

        # create a dictionary with the med obj as the key and the schedule list as values
        med_dict = dict()

        for m in all_meds:
            # if med_dict.get(m):
            #     pass
            # else:
            #     med_dict[m] = m.schedule
            med_dict.setdefault(m, m.schedule)

        # pres_info = {}
        # for pres in all_meds:
        #     pres_info[pres.pres_id] = [pres.med_name, pres.timestamp]
        # print "HELLO! ABOVE IS PRES_INFO!!!!!"

        # should gives back a query for all timestamps from logged in user
        return render_template("prescriptions_dashboard.html",
                               rx_timestamp=rx_timestamp,
                               user=user,
                               meds=all_meds,
                               pres_names=pres_names,
                               # pres_times=pres_times,
                               med_dict=med_dict)
    else:
        flash("User is not logged in.")
        return redirect("/login")


def reminder(user_id):
    # user_id is the parameter
    """Reminds user of when to take their meds."""
    print "IM IN MY REMINDER!!!!!"
    current_dt = datetime.now()
    hour_from_now = current_dt + timedelta(hours=1)
    hour_from_now = hour_from_now.time()
    current_dt = current_dt.time()

    prescription_list = Prescription.query.filter_by(user_id=user_id).all()
    print prescription_list

    for prescription in prescription_list:
        time_of_first_dose = prescription.start_date.time()
        if current_dt <= time_of_first_dose and time_of_first_dose <= hour_from_now:
            # make conditional an hour from now and within current hour
            message = "Reminder: {num_doses} doses {med_name} ".format(
                num_doses=prescription.dosage_quantity,
                med_name=prescription.med_name)
            flash(message)
            return message
            print message
            print "!!!!!" * 20

            # make nav bar in html
            # make sure i'm still being logged in
            # if already logged in, get message that user is already logged in
            # put logged in message in nav bar - make visual - in jinja
            # if "user_id" in session


@app.route('/doctor_registration')
def register_doctor_information():
    """Sends user to fill out doctor information"""
    #Get form variables
    logged_in_user_id = session.get("user_id")
    logged_in_user_email = session.get("email")

    if logged_in_user_id:
        flash("You are currently logged in as %s " % logged_in_user_email)
    else:
        flash("You are not logged in as anyone")
        return redirect("/login")

    return render_template("doctor_registration.html")


@app.route('/process_doctor_registration', methods=["POST"])
def proces_doctor_information():
    """Process user's inputted doctor appointment information from doctor_registration.html"""
    logged_in_user_id = session.get("user_id")
    logged_in_user_email = session.get("email")

    if logged_in_user_id:
        flash("You are currently logged in as %s " % logged_in_user_email)
        doctor_name = request.form.get("doctor_name")
        condition = request.form.get("condition")
        phone = request.form.get("phone")
        office_address = request.form.get("office_address")
        appointment_date = request.form.get("appointment_date")

        print doctor_name + "<== doctor name"
        print condition + "<=== condition name"
        print phone + "<=== phone number of Doctor object"
        print office_address + "<=== office_address"
        print appointment_date + "<===appointment_date"

        new_doctor = Doctor(doctor_name=doctor_name,
                            condition=condition,
                            phone=phone,
                            office_address=office_address,
                            user_id=logged_in_user_id,
                            appointment_date=appointment_date)
        db.session.add(new_doctor)
        db.session.commit()

        # SQL ALCHEMY QUERIES:
        user = User.query.filter_by(user_id=logged_in_user_id).first()

        new_doctors = Doctor.query.filter_by(doctor_name=doctor_name).all()
        print "This below is the doctor_object:"
        print new_doctors
        print "This below is the user object:"
        print user

    else:
        flash("You are not logged in as anyone")
        return redirect("/login")
    return redirect("/your_doctors")


@app.route("/your_doctors")
def display_doctors():

    user = User.query.filter_by(user_id=session['user_id']).first()
    # instead of constaltly using logged_in_user_id, i can just directly get 'user_id' from the session
    all_doctors = Doctor.query.filter_by(user_id=user.user_id).all()

    return render_template("doctors_dashboard.html",
                           all_doctors=all_doctors,
                           user=user)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
