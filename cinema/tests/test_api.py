import pytest
from unittest.mock import patch, MagicMock
from config.utils import get_tmdb_data

@patch("config.utils.requests.get")
def test_get_tmdb_data_success(mock_get):
    """
    Test that get_tmdb_data returns correct data when the API call is successful.
    """
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"title": "Fight Club"}
    mock_get.return_value = fake_response

    result = get_tmdb_data("movie/550")

    mock_get.assert_called_once()
    assert result == {"title": "Fight Club"}



@patch("config.utils.requests.get")
def test_get_tmdb_data_failure(mock_get):
    """
    Test that get_tmdb_data raises an exception when the API call fails.
    """
    fake_response = MagicMock()
    fake_response.status_code = 404
    fake_response.text = "Not Found"
    fake_response.raise_for_status.side_effect = Exception("404 error")
    mock_get.return_value = fake_response

    with pytest.raises(Exception) as exc_info:
        get_tmdb_data("movie/0")

    assert "404" in str(exc_info.value)
