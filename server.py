from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Prescription, Schedule, Doctor
from datetime import datetime, timedelta
# from datetime the module, you're importing datetime the class (both are called datetime)
# static methods are called directly from the class

app = Flask(__name__)

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
    logged_in_user_email = session.get("email")

    if logged_in_user_id:
        reason = request.form.get("reason")
        med_name = request.form.get("med_name")
        side_effects = request.form.get("side_effects")
        starting_amount = int(request.form.get("starting_amount"))
        #starting amount is an integer
        refills_remaining = int(request.form.get("refills_remaining"))
        #refills remaining is an integer
        black_box_warning = request.form.get("black_box_warning")
        first_dose = request.form.get("first_dose")
        last_dose = request.form.get("last_dose")
        dosage_timing = int(request.form.get("dosage_timing"))
        dosage_quantity = int(request.form.get("dosage_quantity"))
        #dosage is a string so no need for an integer
        food = bool(request.form.get("food"))
        water_boolean = bool(request.form.get("water"))
        daily_schedule = request.form.getlist("daily_schedule")


        print water_boolean
        print food
        print first_dose
        print daily_schedule
        print "LOOK AT ME HERE!!!!!!!!!!! ABOVE IS DAILY SCHEDULE TIME!!!!!!!!!!"

        for time_string in daily_schedule:
            print time_string
        #   1.first convert time string into datetime object that's just the time in HOUR:MINUTE:SECONDS format
            timestamp = datetime.strptime(time_string, "%H:%M:%S")
            print timestamp
        #   2. make dosage time object:
        #  ???????????????????????? uh
            new_dosage_time = Schedule(timestamp=timestamp)
            print new_dosage_time
        #   3. do db.add -  #
            db.session.add(new_dosage_time)
            db.session.commit()

        new_prescription = Prescription(user_id=logged_in_user_id,
                                        reason=reason,
                                        med_name=med_name,
                                        side_effects=side_effects,
                                        starting_amount=starting_amount,
                                        refills_remaining=refills_remaining,
                                        black_box_warning=black_box_warning,
                                        first_dose=first_dose,
                                        last_dose=last_dose,
                                        dosage_timing=dosage_timing,
                                        dosage_quantity=dosage_quantity,
                                        food=food,
                                        drink=water_boolean,
                                        schedule=new_dosage_time
                                        )
        db.session.add(new_prescription)
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
        rx_timestamp = Schedule.query.filter_by(schedule_id=logged_in_user_id).all()
        # should gives back a query for all timestamps from logged in user
        return render_template("prescriptions_dashboard.html", meds=all_meds,
                               user=user, rx_timestamp=rx_timestamp)
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
        time_of_first_dose = prescription.first_dose.time()
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

# @app.route('/pass', methods=["PASS"])
# def something():
#     """Something"""

#     return render_template("pass")


# @app.route('/pass', methods=["PASS"])
# def something():
#     """Something"""

#     return render_template("pass")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
