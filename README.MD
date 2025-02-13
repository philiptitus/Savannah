# Savannah API

<p align="center">
  <img src="https://www.svgrepo.com/show/229522/savannah.svg" alt="Savannah Logo" width="200">
</p>

This is a Django project built with Django REST framework.

## Requirements

- Python 3.8+
- Django 3.2+
- Django REST framework 3.12+
- psycopg2 2.8+
- gunicorn 20.0+
- Selenium
- Webdriver Manager

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/philiptitus/Savannah.git
    cd Savannah
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

### Unit Tests

To run the unit tests with coverage checking, follow these steps:

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

### E2E Tests

To run the end-to-end (E2E) tests, you need to have Selenium and Webdriver Manager installed. You can install them using:

```sh
pip install selenium webdriver-manager
```
Then, run the E2E tests using the following command:

```sh

python manage.py test base.test_e2e
```

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

## CI/CD Operations

This project includes a CI/CD pipeline configuration using GitHub Actions. The pipeline is defined in the ci-cd.yml file.

## CI/CD Pipeline Steps

The CI/CD pipeline performs the following steps:

1. **Checkout Code**: Checks out the code from the repository.
2. **Set up Docker Buildx**: Sets up Docker Buildx for building Docker images.
3. **Cache Docker Layers**: Caches Docker layers to speed up the build process.
4. **Install Docker Compose**: Installs Docker Compose.
5. **Build and Push Docker Image**: Builds the Docker image.
6. **Run Docker Compose**: Runs Docker Compose to start the services.
7. **Check Docker Compose Services**: Checks the status of Docker Compose services.
8. **Check Web Service Logs**: Checks the logs of the web service.
9. **Run Tests with Coverage**: Runs the tests with coverage.
10. **Stop Docker Compose**: Stops Docker Compose services.
11. **Install AWS CLI**: Installs the AWS CLI.
12. **Configure AWS Credentials**: Configures AWS credentials.
13. **Make Deploy Script Executable**: Makes the deploy script executable.
14. **Deploy to CodeDeploy**: Deploys the application to AWS CodeDeploy.

## Docker Compose Configuration

The Docker Compose configuration is defined in the `docker-compose.yml` file. It includes the following services:

- **web**: The Django application.
- **db**: The PostgreSQL database.

## Deployment Script

The deployment script is defined in the `deploy.sh` file. It performs the following steps:

1. Navigate to the application directory.
2. Pull the latest changes from the main branch.
3. Stop running containers.
4. Remove all unused containers, networks, images, and optionally, volumes.
5. Build and start the containers.

## AppSpec Configuration

The AppSpec configuration is defined in the `appspec.yml` file. It specifies the files to be copied and the hooks to be executed during the deployment process.

## Links

- [GitHub Repository](https://github.com/philiptitus/Savannah.git)
- [Postman Documentation](https://documenter.getpostman.com/view/31401198/2sAYX9o1RM)
- [Live Deployed Application](https://savapi.duckdns.org/)

## License

This project is licensed under the MIT License.