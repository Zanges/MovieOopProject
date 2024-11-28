import csv
import os

from storage.istorage import IStorage


class StorageCSV(IStorage):
    """ Class for storing movies in a CSV file """
    def __init__(self, file_path: str):
        """
        Constructor for the StorageCSV class

        :param file_path: Path to the CSV file
        """
        self.file_path = file_path

    def _save_movies_data(self, movies_data: dict[str, dict]) -> bool:
        """
        Save the movies data to the file

        :param movies_data:
        """
        try:
            with open(self.file_path, "w", newline="") as fileobj:
                writer = csv.writer(fileobj)
                writer.writerow(["Title", "Year", "Rating", "Poster"])
                for title, details in movies_data.items():
                    writer.writerow([title, details["year"], details["rating"], details["poster"]])
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
            with open(self.file_path, "r", newline="") as fileobj:
                reader = csv.reader(fileobj)
                movies_data = {}
                _ = next(reader)
                for row in reader:
                    title, year, rating, poster = row
                    movies_data[title] = {
                        "year": int(year),
                        "rating": float(rating),
                        "poster": poster
                    }
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
        :param rating: Rating of the movie
        :param poster: URL to the movie poster

        :return: True if the movie was added, False if it already exists
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

        :return: True if the movie was deleted, False if it does not exist
        """
        movies_data = self.list_movies()
        if title not in movies_data:
            return False

        del movies_data[title]
        return self._save_movies_data(movies_data)

    def update_movie(self, title: str, rating: float) -> bool:
        """
        Update a movie in the database, if it exists

        :param title: Name of the movie
        :param year: Release date of the movie
        :param rating: Rating of the movie
        :param poster: URL to the movie poster

        :return: True if the movie was updated, False if it does not exist
        """
        movies_data = self.list_movies()
        if title not in movies_data:
            return False

        movies_data[title]["rating"] = rating
        return self._save_movies_data(movies_data)


def main():
    storage = StorageCSV("movies.csv")
    print(storage.list_movies())
    print(storage.add_movie("The Matrix", 1999, 8.7, "https://www.imdb.com/title/tt0133093/"))
    print(storage.add_movie("The Matrix", 1999, 8.7, "https://www.imdb.com/title/tt0133093/"))
    print(storage.list_movies())
    print(storage.delete_movie("The Matrix"))
    print(storage.delete_movie("The Matrix"))
    print(storage.list_movies())
    print(storage.update_movie("The Matrix", 8.7))
    print(storage.add_movie("The Matrix", 1999, 8.7, "https://www.imdb.com/title/tt0133093/"))
    print(storage.list_movies())
    print(storage.update_movie("The Matrix", 9.0))
    print(storage.list_movies())


if __name__ == "__main__":
    main()