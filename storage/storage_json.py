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
