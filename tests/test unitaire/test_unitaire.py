from tests.conftest import client
import json
from server import loadClubs, loadCompetitions
import pytest


def test_should_index_status_code_ok(client):
    response = client.get("/")
    assert response.status_code == 200


def test_should_public_board_status_code_ok(client):
    response = client.get("/display")
    assert response.status_code == 200


def test_should_summary_status_code_ok(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200


def test_return_to_index_if_bad_email(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.bad"})
    assert "this email doesn&#39;t exist in our club list" in response.data.decode()
    assert response.status_code == 200


def test_fail_message_if_club_or_comp_not_found(client):
    response = client.get("/book/Fall%20Clsic%202/Simply%20Lift")
    assert "Something went wrong-please try again" in response.data.decode()
    assert response.status_code == 200


def test_should_book_status_code_ok(client):
    response = client.get("/book/Spring Festival/Simply Lift")
    assert response.status_code == 200


def test_should_book_competition_not_valid_date(client):
    response = client.get("/book/Spring Festival/Simply Lift")
    assert response.status_code == 200


def test_purchase_in_past_competition(client):
    data = {"competition": "Spring Festival", "club": "Simply Lift", "places": 5}
    response = client.get("book/Spring%20Festival/Simply%20Lift")
    assert "Impossible de réservé des places pour une compétition déja passé" in response.data.decode()
    assert response.status_code == 200


def test_should_purchase_places_status_code_ok(client):
    data = {"competition": "Spring Festival", "club": "Simply Lift", "places": 2}
    response = client.post("/purchasePlaces", data=data)
    assert response.status_code == 200


def test_purchase_more_than_12_places(client):
    data = {"competition": "Spring Festival 2", "club": "Simply Lift", "places": 13}
    response = client.post("/purchasePlaces", data=data)
    assert "No more than 12 places by club!" in response.data.decode()
    assert response.status_code == 200


def test_purchase_more_than_available_places(client):
    data = {"competition": "Spring Festival 2", "club": "Simply Lift", "places": 10}
    response = client.post("/purchasePlaces", data=data)
    assert "not enouth place in this competition!" in response.data.decode()
    assert response.status_code == 200


def test_purchase_more_place_than_point(client):
    data = {"competition": "Fall Classic 2", "club": "Iron Temple", "places": 10}
    response = client.post("/purchasePlaces", data=data)
    assert "have enouth points" in response.data.decode()
    assert response.status_code == 200


def test_should_logout_status_code_ok(client):
    response = client.get("/logout")
    assert response.status_code == 302


def test_load_club():
    clubs = loadClubs()
    assert clubs[0] == {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}


def test_load_competitions():
    competitions = loadCompetitions()
    assert competitions[0] == {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25",
        "valid": False,
    }
