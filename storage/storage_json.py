import json
import os

from storage.istorage import IStorage


class StorageJson(IStorage):
    """ Class for storing movies in a JSON file """
    def __init__(self, file_path: str):
        """
        Constructor for the StorageJson class

        :param file_path: Path to the JSON file
        """
        self.file_path = file_path

    def _save_movies_data(self, movies_data: dict[str, dict]) -> bool:
        """
        Save the movies data to the file

        :param movies_data: dict with movie names as keys and movie details as values

        :return: True if the data was saved, False if an error occurred
        """
        try:
            with open(self.file_path, "w") as fileobj:
                json.dump(movies_data, fileobj)
        except PermissionError:
            print("Could not save the data")
            print("Check if you have the required permissions in:")
            print(f"CWD: {os.getcwd()}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        return True

    def list_movies(self) -> dict[str, dict]:
        """
        List all movies

        :return: dict with movie names as keys and movie details as values
        """
        try:
            if os.path.getsize(self.file_path) == 0:  # Check if the file is empty
                return {}
            with open(self.file_path, "r") as fileobj:
                movies_data = json.load(fileobj)
        except FileNotFoundError:
            movies_data = {}
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Returning empty data")
            movies_data = {}
        return movies_data

    def add_movie(self, title: str, year: int, rating: float, poster: str) -> bool:
        """
        Add a movie to the database, if it does not already exist

        :param title: Name of the movie
        :param year: Release date of the movie
        :param rating: Rating from 0.0 to 10.0
        :param poster: URL of the movie poster

        :return: True if the movie was added, False if the movie already exists
        """
        movies_data = self.list_movies()
        if title in movies_data:
            return False

        movies_data[title] = {
            "year": year,
            "rating": rating,
            "poster": poster
        }
        return self._save_movies_data(movies_data)

    def delete_movie(self, title: str) -> bool:
        """
        Delete a movie from the database, if it exists

        :param title: Name of the movie

        :return: True if the movie was deleted, False if the movie does not exist
        """
        movies_data = self.list_movies()
        if title not in movies_data:
            return False

        del movies_data[title]
        return self._save_movies_data(movies_data)

    def update_movie(self, title: str, rating: float) -> bool:
        """
        Update the rating of a movie, if it exists

        :param title: Name of the movie
        :param rating: New rating of the movie

        :return: True if the movie was updated, False if the movie does not exist
        """
        movies_data = self.list_movies()
        if title not in movies_data:
            return False

        movies_data[title]["rating"] = rating
        return self._save_movies_data(movies_data)


def main():
    storage = StorageJson("movies.json")
    print(storage.list_movies())
    storage.add_movie("The Matrix", 1999, 8.7, "https://www.imdb.com/title/tt0133093/")
    print(storage.list_movies())
    storage.update_movie("The Matrix", 9.0)
    print(storage.list_movies())
    storage.delete_movie("The Matrix")
    print(storage.list_movies())


if __name__ == "__main__":
    main()
