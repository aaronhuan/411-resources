import pytest
import sqlite3
from dataclasses import asdict

from boxing.models.boxers_model import (
    Boxer, create_boxer, delete_boxer, get_leaderboard,
    get_boxer_by_id, get_boxer_by_name, get_weight_class,
    update_boxer_stats
)


@pytest.fixture
def sample_boxer1():
    """Fixture providing a sample boxer for testing."""
    return Boxer(1, "Mike Tyson", 220, 178, 71.0, 25)


@pytest.fixture
def sample_boxer2():
    """Fixture providing a second sample boxer for testing."""
    return Boxer(2, "Muhammad Ali", 215, 191, 78.0, 30)


@pytest.fixture
def mock_db_connection(mocker):
    """Fixture to mock database connection and cursor."""
    mock_conn = mocker.MagicMock()
    mock_cursor = mocker.MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.__exit__.return_value = None
    mock_conn.cursor.return_value = mock_cursor
    return mocker.patch("boxing.models.boxers_model.get_db_connection", return_value=mock_conn)


##################################################
# Boxer Creation and Deletion Test Cases
##################################################


def test_create_boxer_success(mock_db_connection):
    """Test successfully creating a new boxer."""
    mock_cursor = mock_db_connection.return_value.__enter__.return_value.cursor.return_value
    
    create_boxer("Mike Tyson", 220, 178, 71.0, 25)
    
    mock_cursor.execute.assert_called_once()
    mock_cursor.execute.assert_called_with(
        "INSERT INTO boxers (name, weight, height, reach, age) VALUES (?, ?, ?, ?, ?)",
        ("Mike Tyson", 220, 178, 71.0, 25)
    )


def test_create_boxer_duplicate_name(mock_db_connection):
    """Test creating a boxer with a duplicate name."""
    mock_cursor = mock_db_connection.return_value.__enter__.return_value.cursor.return_value
    mock_cursor.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed")
    
    with pytest.raises(ValueError, match="Boxer with name 'Mike Tyson' already exists"):
        create_boxer("Mike Tyson", 220, 178, 71.0, 25)


def test_create_boxer_invalid_weight():
    """Test creating a boxer with invalid weight."""
    with pytest.raises(ValueError, match="Invalid weight: 120. Must be at least 125."):
        create_boxer("Mike Tyson", 120, 178, 71.0, 25)


def test_create_boxer_invalid_height():
    """Test creating a boxer with invalid height."""
    with pytest.raises(ValueError, match="Invalid height: 0. Must be greater than 0."):
        create_boxer("Mike Tyson", 220, 0, 71.0, 25)


def test_create_boxer_invalid_reach():
    """Test creating a boxer with invalid reach."""
    with pytest.raises(ValueError, match="Invalid reach: 0. Must be greater than 0."):
        create_boxer("Mike Tyson", 220, 178, 0, 25)


def test_create_boxer_invalid_age():
    """Test creating a boxer with invalid age."""
    with pytest.raises(ValueError, match="Invalid age: 15. Must be between 18 and 40."):
        create_boxer("Mike Tyson", 220, 178, 71.0, 15)


def test_delete_boxer_success(mock_db_connection):
    """Test successfully deleting a boxer."""
    mock_cursor = mock_db_connection.return_value.__enter__.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = (1,)  # Simulate boxer exists
    
    delete_boxer(1)
    
    mock_cursor.execute.assert_called_once_with("DELETE FROM boxers WHERE id = ?", (1,))


def test_delete_boxer_not_found(mock_db_connection):
    """Test deleting a non-existent boxer."""
    mock_cursor = mock_db_connection.return_value.__enter__.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = None  # Simulate boxer doesn't exist
    
    with pytest.raises(ValueError, match="Boxer with ID 1 not found."):
        delete_boxer(1)


##################################################
# Boxer Retrieval Test Cases
##################################################


def test_get_boxer_by_id_success(mock_db_connection):
    """Test successfully retrieving a boxer by ID."""
    mock_cursor = mock_db_connection.return_value.__enter__.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = (1, "Mike Tyson", 220, 178, 71.0, 25)
    
    boxer = get_boxer_by_id(1)
    
    assert boxer.id == 1
    assert boxer.name == "Mike Tyson"
    assert boxer.weight == 220
    assert boxer.height == 178
    assert boxer.reach == 71.0
    assert boxer.age == 25


def test_get_boxer_by_id_not_found(mock_db_connection):
    """Test retrieving a non-existent boxer by ID."""
    mock_cursor = mock_db_connection.return_value.__enter__.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = None
    
    with pytest.raises(ValueError, match="Boxer with ID 1 not found."):
        get_boxer_by_id(1)


def test_get_boxer_by_name_success(mock_db_connection):
    """Test successfully retrieving a boxer by name."""
    mock_cursor = mock_db_connection.return_value.__enter__.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = (1, "Mike Tyson", 220, 178, 71.0, 25)
    
    boxer = get_boxer_by_name("Mike Tyson")
    
    assert boxer.id == 1
    assert boxer.name == "Mike Tyson"
    assert boxer.weight == 220
    assert boxer.height == 178
    assert boxer.reach == 71.0
    assert boxer.age == 25


def test_get_boxer_by_name_not_found(mock_db_connection):
    """Test retrieving a non-existent boxer by name."""
    mock_cursor = mock_db_connection.return_value.__enter__.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = None
    
    with pytest.raises(ValueError, match="Boxer 'Mike Tyson' not found."):
        get_boxer_by_name("Mike Tyson")


##################################################
# Weight Class Test Cases
##################################################


def test_get_weight_class_heavyweight():
    """Test determining heavyweight class."""
    assert get_weight_class(220) == "HEAVYWEIGHT"


def test_get_weight_class_middleweight():
    """Test determining middleweight class."""
    assert get_weight_class(170) == "MIDDLEWEIGHT"


def test_get_weight_class_lightweight():
    """Test determining lightweight class."""
    assert get_weight_class(140) == "LIGHTWEIGHT"


def test_get_weight_class_featherweight():
    """Test determining featherweight class."""
    assert get_weight_class(130) == "FEATHERWEIGHT"


def test_get_weight_class_invalid():
    """Test determining weight class with invalid weight."""
    with pytest.raises(ValueError, match="Invalid weight: 120. Weight must be at least 125."):
        get_weight_class(120)


##################################################
# Leaderboard Test Cases
##################################################


def test_get_leaderboard_by_wins(mock_db_connection):
    """Test getting leaderboard sorted by wins."""
    mock_cursor = mock_db_connection.return_value.__enter__.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [
        (1, "Mike Tyson", 220, 178, 71.0, 25, 10, 8, 0.8),
        (2, "Muhammad Ali", 215, 191, 78.0, 30, 15, 12, 0.8)
    ]
    
    leaderboard = get_leaderboard("wins")
    
    assert len(leaderboard) == 2
    assert leaderboard[0]["name"] == "Muhammad Ali"
    assert leaderboard[0]["wins"] == 12
    assert leaderboard[1]["name"] == "Mike Tyson"
    assert leaderboard[1]["wins"] == 8


def test_get_leaderboard_by_win_pct(mock_db_connection):
    """Test getting leaderboard sorted by win percentage."""
    mock_cursor = mock_db_connection.return_value.__enter__.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [
        (1, "Mike Tyson", 220, 178, 71.0, 25, 10, 8, 0.8),
        (2, "Muhammad Ali", 215, 191, 78.0, 30, 15, 12, 0.8)
    ]
    
    leaderboard = get_leaderboard("win_pct")
    
    assert len(leaderboard) == 2
    assert leaderboard[0]["win_pct"] == 80.0
    assert leaderboard[1]["win_pct"] == 80.0


def test_get_leaderboard_invalid_sort(mock_db_connection):
    """Test getting leaderboard with invalid sort parameter."""
    with pytest.raises(ValueError, match="Invalid sort_by parameter: invalid"):
        get_leaderboard("invalid")


##################################################
# Boxer Stats Test Cases
##################################################


def test_update_boxer_stats_win(mock_db_connection):
    """Test updating boxer stats for a win."""
    mock_cursor = mock_db_connection.return_value.__enter__.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = (1,)  # Simulate boxer exists
    
    update_boxer_stats(1, "win")
    
    mock_cursor.execute.assert_called_once_with(
        "UPDATE boxers SET fights = fights + 1, wins = wins + 1 WHERE id = ?",
        (1,)
    )


def test_update_boxer_stats_loss(mock_db_connection):
    """Test updating boxer stats for a loss."""
    mock_cursor = mock_db_connection.return_value.__enter__.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = (1,)  # Simulate boxer exists
    
    update_boxer_stats(1, "loss")
    
    mock_cursor.execute.assert_called_once_with(
        "UPDATE boxers SET fights = fights + 1 WHERE id = ?",
        (1,)
    )


def test_update_boxer_stats_invalid_result(mock_db_connection):
    """Test updating boxer stats with invalid result."""
    with pytest.raises(ValueError, match="Invalid result: draw. Expected 'win' or 'loss'."):
        update_boxer_stats(1, "draw")


def test_update_boxer_stats_not_found(mock_db_connection):
    """Test updating stats for non-existent boxer."""
    mock_cursor = mock_db_connection.return_value.__enter__.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = None  # Simulate boxer doesn't exist
    
    with pytest.raises(ValueError, match="Boxer with ID 1 not found."):
        update_boxer_stats(1, "win") 