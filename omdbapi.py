import os
import requests
import dotenv


dotenv.load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")


def get_movie_data(title: str) -> dict:
    """
    Get the movie data from the OMDB API

    :param title: Title of the movie

    :return: dict with movie data
    """
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        raise Exception("Could not get the movie data")
    return response.json()


def format_movie_data(movie_data: dict) -> tuple[bool, dict]:
    """
    Format the movie data

    :param movie_data: dict with movie data

    :return: tuple with a boolean indicating if the movie data is valid, and a dict with the formatted movie data
    """
    if movie_data["Response"] == "False":
        return False, {}
    return True, {
        "title": movie_data["Title"],
        "year": int(movie_data["Year"]),
        "rating": float(movie_data["imdbRating"]),
        "poster": movie_data["Poster"]
    }


def main():
    movie_data = get_movie_data("dgggg")
    print(movie_data)
    formatted_data = format_movie_data(movie_data)
    print(formatted_data)


if __name__ == "__main__":
    main()