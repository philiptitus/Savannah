# Django Project

This is a Django project built with Django REST framework.

## Requirements

- Python 3.8+
- Django 3.2+
- Django REST framework 3.12+
- psycopg2 2.8+
- gunicorn 20.0+

## Installation

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:

    ```sh
    python manage.py migrate
    ```

5. Create a superuser:

    ```sh
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```sh
    python manage.py runserver
    ```

## Usage

- Access the admin panel at `http://127.0.0.1:8000/admin/`
- Access the API endpoints at `http://127.0.0.1:8000/api/`

## Running Tests

To run the tests with coverage checking, follow these steps:

1. Install the `coverage` package if you haven't already:

    ```sh
    pip install coverage
    ```

2. Run the tests with coverage:

    ```sh
    python -m coverage run --source='.' manage.py test
    python -m coverage report
    ```

This will run the tests and generate a coverage report, showing you how much of your code is covered by the tests.

## Deployment

To deploy the project using Gunicorn:

1. Install Gunicorn:

    ```sh
    pip install gunicorn
    ```

2. Run Gunicorn:

    ```sh
    gunicorn <project_name>.wsgi:application
    ```

## License

This project is licensed under the MIT License.