import csv
import datetime
import pytz
import requests
import urllib
import uuid
import pandas as pd

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

# Dictionary of UK cities and their approximate geographic centers
county_centers = uk_cities_coordinates = {
    "Aberdeen": (57.1497, -2.0943),
    "Armagh": (54.3493, -6.6528),
    "Bangor": (53.2270, -4.1293),
    "Bath": (51.3751, -2.3617),
    "Belfast": (54.5973, -5.9301),
    "Birmingham": (52.4862, -1.8904),
    "Bradford": (53.7950, -1.7594),
    "Brighton and Hove": (50.8225, -0.1372),
    "Bristol": (51.4545, -2.5879),
    "Cambridge": (52.2053, 0.1218),
    "Canterbury": (51.2802, 1.0789),
    "Cardiff": (51.4816, -3.1791),
    "Carlisle": (54.8924, -2.9321),
    "Chelmsford": (51.7356, 0.4685),
    "Chester": (53.1910, -2.8957),
    "Chichester": (50.8367, -0.7792),
    "Coventry": (52.4068, -1.5197),
    "Derby": (52.9225, -1.4746),
    "Derry": (55.0068, -7.3183),
    "Dundee": (56.4620, -2.9707),
    "Durham": (54.7753, -1.5849),
    "Edinburgh": (55.9533, -3.1883),
    "Ely": (52.3995, 0.2620),
    "Exeter": (50.7184, -3.5339),
    "Glasgow": (55.8642, -4.2518),
    "Gloucester": (51.8642, -2.2380),
    "Hereford": (52.0567, -2.7161),
    "Inverness": (57.4778, -4.2247),
    "Kingston upon Hull": (53.7676, -0.3274),
    "Lancaster": (54.0466, -2.7990),
    "Leeds": (53.8008, -1.5491),
    "Leicester": (52.6369, -1.1398),
    "Lichfield": (52.6836, -1.8258),
    "Lincoln": (53.2307, -0.5406),
    "Lisburn": (54.5094, -6.0353),
    "Liverpool": (53.4084, -2.9916),
    "London": (51.5074, -0.1278),
    "Londonderry": (55.0068, -7.3183),
    "Manchester": (53.4808, -2.2426),
    "Newcastle upon Tyne": (54.9783, -1.6174),
    "Newport": (51.5842, -2.9977),
    "Norwich": (52.6309, 1.2974),
    "Nottingham": (52.9548, -1.1581),
    "Oxford": (51.7520, -1.2577),
    "Perth": (56.3962, -3.4370),
    "Peterborough": (52.5695, -0.2405),
    "Plymouth": (50.3755, -4.1427),
    "Portsmouth": (50.8198, -1.0873),
    "Preston": (53.7632, -2.7031),
    "Ripon": (54.1381, -1.5245),
    "Salford": (53.4875, -2.2901),
    "Salisbury": (51.0688, -1.7945),
    "Sheffield": (53.3811, -1.4701),
    "Southampton": (50.9097, -1.4044),
    "St Albans": (51.7527, -0.3368),
    "St Asaph": (53.2553, -3.4420),
    "St Davids": (51.8806, -5.2697),
    "Stirling": (56.1165, -3.9369),
    "Sunderland": (54.9069, -1.3838),
    "Swansea": (51.6214, -3.9436),
    "Truro": (50.2653, -5.0547),
    "Wakefield": (53.6833, -1.4977),
    "Wells": (51.2090, -2.6476),
    "Westminster": (51.4975, -0.1357),
    "Winchester": (51.0632, -1.3080),
    "Wolverhampton": (52.5862, -2.1280),
    "Worcester": (52.1920, -2.2200),
    "York": (53.9590, -1.0815),
    "Bangor (Northern Ireland)": (54.6531, -5.6689),
    "Dunfermline": (56.0717, -3.4528),
    "Wrexham": (53.0431, -2.9925),
    "Milton Keynes": (52.0406, -0.7594),
    "Colchester": (51.8892, 0.9042),
    "Doncaster": (53.5228, -1.1285),
    "Middlesbrough": (54.5742, -1.2349),
}

#Code to get the city centers in order to center the map

def get_county_center(target_key):

    target_key_lower = target_key.lower()

    # Iterate over the dictionary
    for key, value in county_centers.items():
        # Check if the current key matches the target key, ignoring case
        if key.lower() == target_key_lower:
            return value

    # Return None if the key is not found
    return None

#To to get the vehicle_codes

vehicle_dict = {
    'Pedal cycle': '01',
    'Motorcycle 50cc and under': '02',
    'Motorcycle over 50cc and up to 125cc': '03',
    'Motorcycle over 125cc and up to 500cc': '04',
    'Motorcycle over 500cc': '05',
    'Motorcycle – unknown cc': '97',
    'Electric motorcycle': '23',
    'Taxi/Private hire car': '08',
    'Car': '09',
    'Minibus (8 - 16 passenger seats)': '10',
    'Bus or coach (17 or more passenger seats)': '11',
    'Ridden horse': '16',
    'Agricultural vehicle (includes diggers etc.)': '17',
    'Tram/Light rail': '18',
    'Van/Goods vehicle 3.5 tonnes maximum gross weight (mgw) and under': '19',
    'Goods vehicle over 3.5 tonnes and under 7.5 tonnes mgw': '20',
    'Goods vehicle 7.5 tonnes mgw and over': '21',
    'Goods vehicle – unknown weight': '98',
    'Mobility scooter': '22',
    'Other vehicle': '90'
}

#Function to extract the frequency of Accidents per day and per hour of the day
def get_stats(data):
    #Extracting Accidents per day of the week
    a=data["day_of_week"].value_counts()
    b =[key for key, value in a.items()]
    c = [value for key, value in a.items()]

    #Extracting Accidents per time of the day
    data2 = [item.replace(':', '') for item in data["time"]]
    hours = [int(str(value)[:2]) for value in data2]
    hours=pd.DataFrame(hours)
    value_counts=hours.value_counts(sort=True)
    x=[key for key, value in value_counts.items()]
    x = [item for (item,) in x]
    y=[value for key, value in value_counts.items()]
    return b,c,x,y
