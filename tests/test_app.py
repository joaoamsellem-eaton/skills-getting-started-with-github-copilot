import pytest
from fastapi.testclient import TestClient

import copy
from src.app import app, activities as app_activities

client = TestClient(app)

# The initial state of activities for test reset
initial_activities = {
    "Basketball Team": {
        "description": "Join the school basketball team and compete in local leagues",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["lucas@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Practice soccer skills and play friendly matches",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": []
    },
    "Drama Club": {
        "description": "Participate in school plays and learn acting techniques",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["mia@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Explore painting, drawing, and other visual arts",
        "schedule": "Fridays, 2:00 PM - 3:30 PM",
        "max_participants": 16,
        "participants": []
    },
    "Math Olympiad": {
        "description": "Prepare for math competitions and solve challenging problems",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 10,
        "participants": ["liam@mergington.edu"]
    },
    "Debate Club": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": []
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    app_activities.clear()
    app_activities.update(copy.deepcopy(initial_activities))

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Basketball Team" in data
    assert "Soccer Club" in data
    assert "Drama Club" in data

def test_signup_and_unregister():
    # Sign up a new participant
    activity = "Soccer Club"
    email = "testuser@example.com"
    signup_url = f"/activities/{activity}/signup?email={email}"
    unregister_url = f"/activities/{activity}/unregister?email={email}"

    # Ensure not already signed up
    client.post(unregister_url)

    # Sign up
    response = client.post(signup_url)
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post(signup_url)
    assert response.status_code == 400

    # Unregister
    response = client.post(unregister_url)
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

    # Unregister again should fail
    response = client.post(unregister_url)
    assert response.status_code == 400
