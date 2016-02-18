from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Prescription, Schedule, Doctor

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

    flash("Logged in")
    return redirect("/")
    # where to direct this page?


@app.route('/logout', methods=['GET'])
def logout():
    """Log out."""

    # del session["user_id"]
    # del session["email"]
    # del session["first_name"]
    session.clear()
    flash("User Logged out.")
    return redirect("/")


@app.route('/register', methods=['GET'])
def register():
    """Sends user to fill out medicine information"""
    #Get form variables

    return render_template("register.html")


@app.route('/medication', methods=['POST'])
def submittal():
    """Getting variables from medication registeration form"""
    logged_in_user_id = session.get("user_id")
    if logged_in_user_id:
        reason = request.form.get("reason")
        med_name = request.form.get("med_name")
        side_effects = request.form.get("side_effects")
        starting_amount = int(request.form.get("starting_amount"))
        #starting amount is an integer
        refills_remaining = int(request.form.get("refills_remaining"))
        #refills remaining is an integer
        black_box_warning = request.form.get("black_box_warning")
        dosage_timing = request.form.get("dosage_timing")
        dosage_quantity = request.form.get("dosage_quantity")
        #dosage is a string so no need for an integer
        food = bool(request.form.get("food"))
        water_boolean = bool(request.form.get("water"))
        print water_boolean
        print food

        new_prescription = Prescription(user_id=logged_in_user_id,
                                        reason=reason,
                                        med_name=med_name,
                                        side_effects=side_effects,
                                        starting_amount=starting_amount,
                                        refills_remaining=refills_remaining,
                                        black_box_warning=black_box_warning,
                                        dosage_timing=dosage_timing,
                                        dosage_quantity=dosage_quantity,
                                        food=food,
                                        drink=water_boolean)
        print new_prescription
        db.session.add(new_prescription)
        db.session.commit()

        flash("Medication %s added." % med_name)
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
        return render_template("prescriptions_dashboard.html", meds=all_meds,
                               user=user)
    else:
        flash("User is not logged in.")
        return redirect("/login")

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
