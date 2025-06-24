import pytest
from rest_framework.test import APIClient
from films.models import Movie

@pytest.mark.django_db
def test_filter_by_status():
    """
    Test the movie list endpoint with status filter.
    Ensures that only movies with the specified status are returned.
    """
    Movie.objects.create(
        title="Planned Movie",
        overview="A planned movie.",
        release_date="2027-01-01",
        rating=0,
        status="planned",
        source="manual"
    )
    Movie.objects.create(
        title="Released Movie",
        overview="A released movie.",
        release_date="2024-01-01",
        rating=5,
        status="released",
        source="manual"
    )

    client = APIClient()
    response = client.get("/api/movies/by-status/?status=planned")
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["title"] == "Planned Movie"