from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import app, activities


INITIAL_ACTIVITIES = deepcopy(activities)


def reset_activities():
    activities.clear()
    activities.update(deepcopy(INITIAL_ACTIVITIES))


def test_get_activities_returns_all_activities():
    # Arrange
    reset_activities()
    client = TestClient(app)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, dict)
    assert "Chess Club" in json_data
    assert json_data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_for_activity_adds_participant():
    # Arrange
    reset_activities()
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_duplicate_signup_returns_bad_request():
    # Arrange
    reset_activities()
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_from_activity():
    # Arrange
    reset_activities()
    client = TestClient(app)
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_signup_invalid_activity_returns_not_found():
    # Arrange
    reset_activities()
    client = TestClient(app)

    # Act
    response = client.post("/activities/UnknownActivity/signup?email=test@mergington.edu")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_invalid_activity_returns_not_found():
    # Arrange
    reset_activities()
    client = TestClient(app)

    # Act
    response = client.delete("/activities/UnknownActivity/signup?email=test@mergington.edu")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
