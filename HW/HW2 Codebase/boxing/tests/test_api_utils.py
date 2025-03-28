import pytest
import requests

from boxing.utils.api_utils import get_random


def test_get_random_success(mocker):
    """Test successfully getting a random number from random.org."""
    # Mock the requests.get function to return a successful response
    mock_response = mocker.MagicMock()
    mock_response.text = "0.75\n"
    mock_response.raise_for_status.return_value = None
    mocker.patch("requests.get", return_value=mock_response)

    result = get_random()
    assert result == 0.75


def test_get_random_invalid_response(mocker):
    """Test handling invalid response from random.org."""
    # Mock the requests.get function to return an invalid response
    mock_response = mocker.MagicMock()
    mock_response.text = "invalid\n"
    mock_response.raise_for_status.return_value = None
    mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(ValueError, match="Invalid response from random.org: invalid"):
        get_random()


def test_get_random_timeout(mocker):
    """Test handling timeout from random.org."""
    # Mock the requests.get function to raise a timeout exception
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout())

    with pytest.raises(RuntimeError, match="Request to random.org timed out."):
        get_random()


def test_get_random_request_error(mocker):
    """Test handling request error from random.org."""
    # Mock the requests.get function to raise a request exception
    mocker.patch("requests.get", side_effect=requests.exceptions.RequestException("Connection error"))

    with pytest.raises(RuntimeError, match="Request to random.org failed: Connection error"):
        get_random()


def test_get_random_http_error(mocker):
    """Test handling HTTP error from random.org."""
    # Mock the requests.get function to raise an HTTP error
    mock_response = mocker.MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
    mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(RuntimeError, match="Request to random.org failed: 404 Not Found"):
        get_random() 