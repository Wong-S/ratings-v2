"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route("/")
def create_homepage():
    """Return homepage"""

    return render_template("homepage.html")


@app.route("/movies")
def all_movies():
    """Return a list of all movies"""

    movies = crud.get_movies()

    return render_template("all_movies.html", movies=movies)


@app.route("/movies/<movie_id>")
def show_movie(movie_id):
    """Show details on a particular movie"""

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)


# End of part 3 Section: Create a list of users at /users
@app.route("/users")
def display_users_email():
    """Show all users email addresses and link to user's profile"""

    users_emails = crud.get_user_email()

    return render_template("user_details.html", users_emails=users_emails)


@app.route("/users/<user_id>")
def display_user_profile(user_id):
    """Show user's profile containing user's email"""

    user_profile = crud.get_user_by_id(user_id)

    return render_template("user_profile.html", user_profile=user_profile)


# Part 4 Starts here:
@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user"""

    email = request.form.get("email")
    password = request.form.get("password")

    check_email = crud.get_user_by_email(email)

    # pseudocode:
    # if check_email.email == email:
    #     flash("Email is associated with an account")
    # else:
    #     crud.create_user(email, password)
    #     flash("New account created successfully!")

    if check_email == None:
        crud.create_user(email, password)
        flash("New account created successfully! Please log in")
    else:
        flash("Email is associated with an account. Try again")

    return redirect("/")


@app.route("/login")
def check_login_credentials():

    email = request.args.get("login_email")
    password = request.args.get("login_password")

    match_passwords = crud.check_password(email, password)

    if match_passwords == True:
        flash("Logged in!")
    else:
        flash("OH NO!")

    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
