from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Prescription, Schedule, Doctor

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
#???

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

    #request.args.getlist from a checklist form. that checklist will contian little boxes
    #list should give back a list of times
    #each item from the checklist is its own row


@app.route('/register', methods=['GET'])
def register():
    """Sends user to fill out medicine information"""
    #Get form variables

    return render_template("register.html")


@app.route('/medication', methods=['POST'])
def submittal():
    """Getting variables from medication registeration form"""
    reason = request.form.get("reason")
    med_name = request.form.get("med_name")
    side_effects = request.form.get("side_effects")
    starting_amount = int(request.form.get("starting_amount"))
    #starting amount is an integer
    refills_remaining = int(request.form.get("refills_remaining"))
    #refills remaining is an integer
    black_box_warning = request.form.get("black_box_warning")
    dosage = request.form.get("dosage")
    #dosage is a string so no need for an integer
    food = bool(request.form.get("food"))
    water_boolean = bool(request.form.get("water"))
    print water_boolean
    print food

    new_prescription = Prescription(reason=reason,
                                    med_name=med_name,
                                    side_effects=side_effects,
                                    starting_amount=starting_amount,
                                    refills_remaining=refills_remaining,
                                    black_box_warning=black_box_warning,
                                    dosage=dosage,
                                    food=food,
                                    water=water_boolean)
    print new_prescription
    db.session.add(new_prescription)
    db.session.commit()

    flash("Medication %s added." % med_name)
    return redirect("/")

# @app.route('/pass', methods=["PASS"])
# def something():
#     """Something"""

#     return render_template("pass")


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
