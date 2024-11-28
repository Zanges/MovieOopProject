from abc import ABC, abstractmethod


class IStorage(ABC):
    """ Interface for the storage module """
    @abstractmethod
    def _save_movies_data(self, movies_data: dict[str, dict]) -> bool:
        """
        Save the movies data to the file

        :param movies_data:
        """
        pass

    @abstractmethod
    def list_movies(self) -> dict[str, dict]:
        """
        List all movies

        :return: dict with movie names as keys and movie details as values
        """
        pass

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
