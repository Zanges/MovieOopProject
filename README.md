# My Movie App

This is a simple command-line application to manage a list of movies with their details.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

Make sure you have Python and pip installed on your machine.
You need an https://www.omdbapi.com/ API key to fetch movie details.

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

3. **Set the API key:** 

    create a file named `.env` in the root directory of the project and add the following line:
    ```sh
    OMDB_API_KEY=*your_api_key*
    ```
    Replace `*your_api_key*` with your actual API key.

### Running the Application

1. **Run the application:**

    ```sh
    python main.py
    ```

2. **You can also specify a storage file (json/csv) as an argument:**

    ```sh
    python main.py movies.json
    ```

You should now be able to interact with the movie list through the command-line interface.