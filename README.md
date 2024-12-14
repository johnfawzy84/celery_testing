# celery_testing
Celery Testing

## How to start this project

1. Clone the repository:
   ```sh
   git clone https://github.com/johnfawzy84/celery_testing.git
   cd celery_testing
   ```

2. Install Poetry:
   ```sh
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. Install dependencies:
   ```sh
   poetry install
   ```

4. Activate the virtual environment:
   ```sh
   poetry shell
   ```

5. Start the services using Docker Compose:
   ```sh
   docker-compose up
   ```

6. Run the FastAPI application:
   ```sh
   uvicorn main:app --reload
   ```

7. Open your browser and go to `http://localhost:8000` to see the FastAPI application running.

8. To run the tests:
   ```sh
   pytest
   ```
