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


@app.route('/register')
def something():
    """Sends user to fill out medicine information"""

    return render_template("register.html")


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
