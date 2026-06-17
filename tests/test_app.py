from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities_returns_activities():
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    json_data = response.json()
    assert expected_activity in json_data
    assert "description" in json_data[expected_activity]
    assert "participants" in json_data[expected_activity]


def test_signup_for_activity_adds_participant():
    # Arrange
    activity_name = "Programming Class"
    new_email = "testuser@mergington.edu"
    initial_participants = list(activities[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={new_email}")

    # Assert
    assert response.status_code == 200
    assert new_email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == len(initial_participants) + 1
    assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"


def test_signup_for_activity_duplicate_returns_400():
    # Arrange
    activity_name = "Chess Club"
    duplicate_email = activities[activity_name]["participants"][0]

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={duplicate_email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_for_invalid_activity_returns_404():
    # Arrange
    activity_name = "Nonexistent Club"
    new_email = "ghost@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={new_email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
