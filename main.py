from movie_app import MovieApp
from storage.storage_json import StorageJson


def main():
    storage = StorageJson("movies.json")
    app = MovieApp(storage)
    app.run()


if __name__ == '__main__':
    main()