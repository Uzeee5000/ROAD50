import os
import pandas as pd
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import gmplot
import sqlite3
from helpers import get_county_center, vehicle_dict, get_stats


from helpers import apology, login_required

# Configure application
app = Flask(__name__)


con=sqlite3.connect("accident_data.db", check_same_thread=False)
cur=con.cursor()


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///accident_data.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




@app.route("/")
@login_required
def home():
    """Show frequency of Accidents"""
    #Extracting Accidents frequency per day and per hour of the day from the database
    accident = pd.read_sql_query("SELECT day_of_week,time FROM accident  WHERE accident_year=2020;", con)

    b,c,x,y=get_stats(accident)
    return render_template("home.html", xArray=b, yArray=c,xArray2=x,yArray2=y)


@app.route("/vehicles", methods=["GET", "POST"])
@login_required
def vehicle():
    """Show Accident statistics per day and per hour"""

    if request.method == "GET":
        x=[key for key, value in vehicle_dict.items()]
        return render_template("vehicles.html",symbols=x)
    else:
        vehicle = request.form.get("vehicle_type")
        #Error Checking for user input
        if not vehicle:
            return apology("must provide vehicle type", 400)
        #Plotting the selected vehicle type statistics
        vehicle=vehicle_dict[vehicle]
        query = f"""
        SELECT a.time,a.day_of_week, v.vehicle_type
        FROM accident AS a
        JOIN vehicle AS v ON a.accident_index = v.accident_index
        WHERE v.vehicle_type={vehicle} AND a.accident_year=2020
        """
        data = pd.read_sql_query(query, con)
        b,c,x,y=get_stats(data)

        return render_template("vplot.html", xArray=b, yArray=c,xArray2=x,yArray2=y)


@app.route("/history")
@login_required
def history():
    """Show preacautionary measures that can be taken"""
    return render_template("history.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
# Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        #Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)
        #Ensure Passwords are same
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)

        #Query database for inserted username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )
        if len(rows) !=0:
            return apology("username already exists",400)

        #Inserting username and password hash into database
        db.execute("INSERT INTO users(username,hash) VALUES(?,?)",
                   request.form.get("username"),generate_password_hash(request.form.get("password")))

        #logging in user
        rows=db.execute("SELECT * FROM users WHERE username=?",request.form.get("username"))
        session["user_id"]=rows[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")

#Defining Areas and police codes
Areas=["Metropolitan Police", "Cumbria", "Lancashire", "Merseyside", "Greater Manchester", "Cheshire", "Northumbria", "Durham", "North Yorkshire", "West Yorkshire", "South Yorkshire", "Humberside", "Cleveland", "West Midlands", "Staffordshire", "West Mercia", "Warwickshire", "Derbyshire", "Nottinghamshire", "Lincolnshire", "Leicestershire", "Northamptonshire", "Cambridgeshire", "Norfolk", "Suffolk", "Bedfordshire", "Hertfordshire", "Essex", "Thames Valley", "Hampshire", "Surrey", "Kent", "Sussex", "City of London", "Devon and Cornwall", "Avon and Somerset", "Gloucestershire", "Wiltshire", "Dorset ", "North Wales", "Gwent", "South Wales", "Dyfed-Powys", "Northern", "Grampian", "Tayside", "Fife", "Lothian and Borders", "Central", "Strathclyde", "Dumfries and Galloway"]
police_codes=[1,3,4,5,6,7,10,11,12,13,14,16,17,20,21,22,23,30,31,32,33,34,35,36,37,40,41,42,43,44,45,46,47,48,50,52,53,54,55,60,61,62,63,91,92,93,94,95,96,97,98]
Area_Codes=dict(zip(Areas,police_codes))


def is_provided(field):
    if not request.form.get(field):
        return apology(f"Must provide {field}", 400)

@app.route("/mapping", methods=["GET", "POST"])
@login_required
def mapping():
    """Sell shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        coordinates = request.form.get("coordinates")

        #Error Checking for Input
        find_missing_errors = is_provided("symbol") or is_provided("coordinates")
        if find_missing_errors:
            return find_missing_errors
        elif get_county_center(coordinates) is None:
            return apology("Must provide a valid City name", 400)

        # Define the police_force variable
        police_force_value = Area_Codes[symbol]

        # Create a SQL query to extract the relevant data
        query = f"""
                SELECT * FROM accident
                WHERE police_force={police_force_value} AND accident_year=2020
                """
        data = pd.read_sql_query(query, con)
        # Plotting the extracted coordinates using gmplot library
        longitude=data["longitude"]
        latitude=data["latitude"]
        a=get_county_center(coordinates)
        x=a[0]
        y=a[1]
        gmap = gmplot.GoogleMapPlotter(x, y, 12 )
        gmap.scatter( latitude, longitude,
                                size = 40, marker = False)
        #Plotting the unique file for every user with name same as their unique user_id
        filename=str(session["user_id"])
        gmap.draw(f"static/{filename}.html")

        return render_template("map.html",plot_filename=f"{filename}.html")
    else:
        return render_template("mapping.html", symbols=Areas)
