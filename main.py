from movie_app import MovieApp
from storage.storage_json import StorageJson
from storage.storage_csv import StorageCSV


def main():
    while True:
        storage_choice = input("Which storage file do you want to use(json/csv)? Enter the file name or press enter for default[movies.json]: ")
        if storage_choice == "":
            storage = StorageJson("movies.json")
            break
        if storage_choice.endswith(".json"):
            storage = StorageJson(storage_choice)
            break
        if storage_choice.endswith(".csv"):
            storage = StorageCSV(storage_choice)
            break
        print("Invalid file name. Please try again.")

    app = MovieApp(storage)
    app.run()


if __name__ == '__main__':
    main()