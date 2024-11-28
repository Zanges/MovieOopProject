import os
import tempfile

import pytest

from storage.storage_json import StorageJson
from storage.storage_csv import StorageCSV


"""
All tests are passing, but I get a debug message that's indicating that there's a problem loading the data from the files. Why does this occur?

OUTPUT:
```
test_storage.py::TestStorageJson::test_list_movies_empty PASSED          [ 12%]An error occurred: Expecting value: line 1 column 1 (char 0)
Returning empty data
```
"""
class TestStorageJson:
    @pytest.fixture
    def storage(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file_path = temp_file.name

        storage = StorageJson(file_path)
        yield storage

        if os.path.exists(file_path):
            os.remove(file_path)

    def test_list_movies_empty(self, storage):
        assert storage.list_movies() == {}

    def test_add_movie(self, storage):
        assert storage.add_movie("The Matrix", 1999, 8.7, "https://www.imdb.com/title/tt0133093/") is True
        assert storage.list_movies() == {
            "The Matrix": {
                "year": 1999,
                "rating": 8.7,
                "poster": "https://www.imdb.com/title/tt0133093/"
            }
        }

    def test_update_movie(self, storage):
        storage.add_movie("The Matrix", 1999, 8.7, "https://www.imdb.com/title/tt0133093/")
        assert storage.update_movie("The Matrix", 9.0) is True
        assert storage.list_movies() == {
            "The Matrix": {
                "year": 1999,
                "rating": 9.0,
                "poster": "https://www.imdb.com/title/tt0133093/"
            }
        }

    def test_delete_movie(self, storage):
        storage.add_movie("The Matrix", 1999, 8.7, "https://www.imdb.com/title/tt0133093/")
        assert storage.delete_movie("The Matrix") is True
        assert storage.list_movies() == {}


class TestStorageCSV:
    @pytest.fixture
    def storage(self):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file_path = temp_file.name

        storage = StorageCSV(file_path)
        yield storage

        if os.path.exists(file_path):
            os.remove(file_path)

    def test_list_movies_empty(self, storage):
        assert storage.list_movies() == {}

    def test_add_movie(self, storage):
        assert storage.add_movie("The Matrix", 1999, 8.7, "https://www.imdb.com/title/tt0133093/") is True
        assert storage.list_movies() == {
            "The Matrix": {
                "year": 1999,
                "rating": 8.7,
                "poster": "https://www.imdb.com/title/tt0133093/"
            }
        }

    def test_update_movie(self, storage):
        storage.add_movie("The Matrix", 1999, 8.7, "https://www.imdb.com/title/tt0133093/")
        assert storage.update_movie("The Matrix", 9.0) is True
        assert storage.list_movies() == {
            "The Matrix": {
                "year": 1999,
                "rating": 9.0,
                "poster": "https://www.imdb.com/title/tt0133093/"
            }
        }

    def test_delete_movie(self, storage):
        storage.add_movie("The Matrix", 1999, 8.7, "https://www.imdb.com/title/tt0133093/")
        assert storage.delete_movie("The Matrix") is True
        assert storage.list_movies() == {}