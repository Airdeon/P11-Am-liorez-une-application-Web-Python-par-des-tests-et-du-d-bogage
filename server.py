import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        for competitions in listOfCompetitions:
            if datetime.strptime(competitions["date"], "%Y-%m-%d %H:%M:%S") < datetime.now():
                competitions["valid"] = False
            else:
                competitions["valid"] = True
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"


def config_app(config):
    app.config.from_object(config)
    return app


competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    if not any(email["email"] == request.form["email"] for email in clubs):
        flash("this email doesn't exist in our club list")
        return render_template(
            "index.html",
        )
    else:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
        )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html",
            club=foundClub,
            competition=foundCompetition,
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    if placesRequired > 12:
        flash("No more than 12 places by club!")
        return render_template("booking.html", club=club, competition=competition)
    elif placesRequired > int(competition["numberOfPlaces"]):
        flash("not enouth place in this competition!")
        return render_template("booking.html", club=club, competition=competition)
    elif placesRequired > int(club["points"]):
        flash("you don't have enouth points")
        flash("points : " + str(club["points"]))
        return render_template("booking.html", club=club, competition=competition)
    else:
        competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
        club["points"] = int(club["points"]) - placesRequired
        flash("Great-booking complete!")
        return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display
@app.route("/display")
def display():
    return render_template("display.html", public_list=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
