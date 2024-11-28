import math
import os
import random

from storage.istorage import IStorage
from user_input import get_valid_arguments
from storage.storage_json import StorageJson
from omdbapi import get_movie_data, format_movie_data


class MovieApp:
    @staticmethod
    def _print_movie(movie_name: str, movie_data: dict) -> None:
        """ Print a movie """
        print(f"Movie: {movie_name}")
        print(f"\tRelease Date: {movie_data['year']}")
        print(f"\tRating: {movie_data['rating']}")

    @staticmethod
    def _command_graceful_exit() -> None:
        """ Gracefully exit the program """
        print("Exiting the program...")
        exit(0)

    def __init__(self, storage: IStorage, app_name: str = "Movie App"):
        self.storage = storage
        self.app_name = app_name

        self.commands = [ # !IMPORTANT! args have to be in the same order as the function arguments
            {
                "function": self._command_graceful_exit,
                "description": "Exit the program",
                "args": [],
            },
            {
                "function": self._command_generate_website,
                "description": "Generate a website with all movies",
                "args": [],
            },
            {
                "function": self._command_add_movie,
                "description": "Add a new movie",
                "args": ["Movie Name"],
            },
            {
                "function": self._command_remove_movie,
                "description": "Remove a movie",
                "args": ["Movie Name"],
            },
            # {
            #     "function": self._command_edit_movie,
            #     "description": "Edit a movies rating",
            #     "args": ["Movie Name", "New Rating"],
            # },
            {
                "function": self._command_list_movies,
                "description": "List all movies",
                "args": [],
            },
            {
                "function": self._command_list_movies_sorted_by_rating,
                "description": "Print all movies sorted by rating",
                "args": ["Ascending/Descending"],
            },
            {
                "function": self._command_list_movies_sorted_by_release_date,
                "description": "Print all movies sorted by release date",
                "args": ["Ascending/Descending"],
            },
            {
                "function": self._command_print_random_movie,
                "description": "Print a random movie",
                "args": [],
            },
            {
                "function": self._command_fuzzy_search,
                "description": "Fuzzy search for a movie",
                "args": ["Search Term"],
            },
            {
                "function": self._command_filter_movies,
                "description": "Filter movies by rating and release date",
                "args": ["Min Rating", "Start Year", "End Year"],
            },
            {
                "function": self._command_print_statistics,
                "description": "Print statistics about the movies",
                "args": [],
            },
        ]

    def run(self) -> None:
        """ Run the movie app """
        print("Welcome to the movie app!")
        while True:
            self._list_commands()
            try:
                command_index = int(input("Enter a command number: "))
            except ValueError:
                print("Invalid command number")
                continue
            if command_index < 0 or command_index >= len(self.commands):
                print("Invalid command number")
                continue
            self._execute_command(command_index)

    def _execute_command(self, command_index: int) -> None:
        """ Execute a command with the given index """
        command = self.commands[command_index]
        print(f"Executing command: {command['description']}")
        args = get_valid_arguments(command["args"])
        command["function"](*args)

    def _list_commands(self) -> None:
        """ List all available commands """
        for i, command in enumerate(self.commands):
            print(f"[{i}] {command['description']}")

    def _command_add_movie(self, movie_name: str) -> None:
        """ Add a new movie """
        try:
            api_movie_data = get_movie_data(movie_name)
        except Exception as e:
            print(f"Could not get the movie data: {e}")
            return
        success, movie_data = format_movie_data(api_movie_data)
        if not success:
            print("Could not get the movie data for:", movie_name)
            print("Please check the movie name and try again")
            return
        self.storage.add_movie(movie_data["title"], movie_data["year"], movie_data["rating"], movie_data["poster"])

    def _command_remove_movie(self, movie_name: str) -> None:
        """ Remove a movie """
        self.storage.delete_movie(movie_name)

    def _command_edit_movie(self, movie_name: str, new_rating: float) -> None:
        """ Edit a movies rating """
        self.storage.update_movie(movie_name, new_rating)

    def _command_list_movies(self) -> None:
        """ List all movies """
        movies = self.storage.list_movies()
        for movie_name, movie in movies.items():
            MovieApp._print_movie(movie_name, movie)

    def _command_list_movies_sorted_by_rating(self, ascending: bool) -> None:
        """ List all movies sorted by rating """
        movies = self.storage.list_movies()
        sorted_movies = sorted(
            movies.items(),
            key=lambda item_tuple: item_tuple[1]['rating'],
            reverse=not ascending
        )

        for movie_name, movie_data in sorted_movies:
            MovieApp._print_movie(movie_name, movie_data)

    def _command_list_movies_sorted_by_release_date(self, ascending: bool) -> None:
        """ List all movies sorted by release date """
        movies = self.storage.list_movies()
        sorted_movies = sorted(
            movies.items(),
            key=lambda item_tuple: item_tuple[1]['year'],
            reverse=not ascending
        )

        for movie_name, movie_data in sorted_movies:
            MovieApp._print_movie(movie_name, movie_data)

    def _command_print_random_movie(self) -> None:
        """ Print a random movie """
        movies = self.storage.list_movies()
        random_movie_name = random.choice(list(movies.keys()))
        MovieApp._print_movie(random_movie_name, movies[random_movie_name])

    def _command_fuzzy_search(self, search_term: str) -> None:
        """ Fuzzy search for a movie """
        movies = self.storage.list_movies()
        found_movies = {}
        for movie_name in movies:
            if search_term.lower() in movie_name.lower():
                found_movies[movie_name] = movies[movie_name]
        if not found_movies:
            print(f'No movies found with the partial name "{search_term}"')
            return
        print(f'Movies found with the partial name "{search_term}":')
        for found_movie_name, found_movie_data in found_movies.items():
            MovieApp._print_movie(found_movie_name, found_movie_data)

    def _command_filter_movies(self, minimum_rating: float, start_year: int, end_year: int) -> None:
        """ Filter movies by rating and release date """
        movies = self.storage.list_movies()
        found_movies = {}
        for movie_name, movie_data in movies.items():
            if minimum_rating <= movie_data['rating'] and start_year <= movie_data['year'] <= end_year:
                found_movies[movie_name] = movie_data
        if not found_movies:
            print("No movies found with the given filters")
            return
        print("Movies found with the given filters:")
        for found_movie_name, found_movie_data in found_movies.items():
            MovieApp._print_movie(found_movie_name, found_movie_data)

    def _command_print_statistics(self) -> None:
        """ Print statistics about the movies """
        movies = self.storage.list_movies()
        total_movies = len(movies)
        ratings = [movie_data['rating'] for movie_data in movies.values()]
        average_rating = sum(ratings) / total_movies if total_movies > 0 else 0
        if len(ratings) % 2 == 0:
            half_len = len(ratings) / 2
            median_rating = (ratings[math.floor(half_len)] + ratings[math.ceil(half_len)]) / 2
        else:
            median_rating = ratings[len(ratings) // 2]
        print(f"Total movies: {total_movies}")
        print(f"Average rating: {average_rating:.1f}")
        print(f"Median rating: {median_rating:.1f}")

        best_movie_rating = max(ratings, default=0)
        best_movies = [
            (movie_name, movie_data)
            for movie_name, movie_data
            in movies.items()
            if movie_data['rating'] == best_movie_rating
        ]
        if best_movies:
            if len(best_movies) == 1:
                print("Best movie:")
            else:
                print("Best movies:")
            for best_movie_name, best_movie_data in best_movies:
                MovieApp._print_movie(best_movie_name, best_movie_data)

        worst_movie_rating = min(ratings, default=0)
        worst_movies = [
            (movie_name, movie_data)
            for movie_name, movie_data
            in movies.items()
            if movie_data['rating'] == worst_movie_rating
        ]
        if worst_movies:
            if len(worst_movies) == 1:
                print("Worst movie:")
            else:
                print("Worst movies:")
            for worst_movie_name, worst_movie_data in worst_movies:
                MovieApp._print_movie(worst_movie_name, worst_movie_data)

    def _command_generate_website(self):
        """ Generate a website with all movies """
        if not os.path.exists("./_static/index_template.html"):
            print("The movie grid template file does not exist")
            return

        movies = self.storage.list_movies()
        movie_grid_content = ""
        for movie_name, movie_data in movies.items():
            movie_grid_content += (
                f'<li>\n'
                f'<div class="movie">\n'
                f'<img class="movie-poster" src="{movie_data["poster"]}" alt="{movie_name} Poster">\n'
                f'<div class="movie-title">{movie_name}</div>\n'
                f'<div class="movie-year">{movie_data["year"]}</div>\n'
                f'</div>\n'
                f'</li>\n'
            )

        with open("./_static/index_template.html", "r") as fileobj:
            movie_grid_template = fileobj.read()

        new_html = (movie_grid_template
                    .replace("__TEMPLATE_TITLE__", self.app_name)
                    .replace("__TEMPLATE_MOVIE_GRID__", movie_grid_content)
                    )

        with open("./_static/index.html", "w") as fileobj:
            fileobj.write(new_html)

        print("Website generated successfully")
        while True:
            user_input = input("Do you want to open the website? (Y/n)")
            if user_input == "" or user_input.lower() == "y":
                os.system("start _static/index.html")
                break
            elif user_input.lower() == "n":
                break


def main():
    storage = StorageJson("movies.json")
    app = MovieApp(storage)
    app.run()


if __name__ == '__main__':
    main()