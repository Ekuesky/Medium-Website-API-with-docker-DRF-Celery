# Medium Website API with Docker, DRF, Celery, and More

This project demonstrates how to build a functional REST API using Django Rest Framework (DRF), Docker, Celery, and other essential tools. 

## Key Features

1. **Built with Docker:** Leveraging Docker for containerization, enabling seamless deployment and scalability.
2. **Asynchronous Tasks with Celery and Redis:** Utilizing Celery and Redis for background tasks, improving application responsiveness.
3. **API Testing with Pytest:** Comprehensive API testing with Pytest, ensuring code quality and reliability.
4. **Token-Based Authentication:** Secure user authentication with token-based authentication.
5. **Email Handling:**  Email integration for both development (Mailhog) and production (Mailgun).
6. **Static and Media Files Serving:** Efficient serving of static and media files with NGINX and whitenoise.

## Concepts Covered

This project covers various essential concepts, including:

* **Docker and Multi-Container Management:** Running and managing multiple Docker containers.
* **Securing Django REST API with HTTPS:** Implementing SSL certificates for API security.
* **REST API Development with Django and DRF:** Building robust REST APIs using Django and DRF.
* **Class-Based Views:** Implementing API endpoints using class-based views for improved code organization.
* **Shell Scripting:** Automating tasks and deployments with shell scripts.
* **Asynchronous Tasks Monitoring with Flower:** Monitoring and managing Celery tasks with Flower.
* **Token-Based Authentication:** Secure user authentication using token-based mechanisms.
* **Email Integration with Mailhog and Mailgun:** Handling email communication in development and production.
* **Python Test Coverage:** Measuring and improving code coverage with testing tools.
* **Serving Static and Media Files:** Efficiently serving static and media files with NGINX and whitenoise.
* **Makefiles for Docker Workflow:** Simplifying Docker tasks and deployments with Makefiles.

## Getting Started

**Prerequisites:**

* Docker and Docker Compose
* Python 3.x

**Steps:**

1. Clone the repository: `git clone https://github.com/Ekuesky/Medium-Website-API-with-docker-DRF-Celery`
2. Navigate to the project directory: `cd Medium-Website-API-with-docker-DRF-Celery`
3. Build and run the Docker containers: `make build`
4. Access the API documentation (Swagger/Redoc): [localhost:8080/redoc]
5. Create a superuser `make superuser`
6. Access the admin panel  [localhost:8080/hidden]
7. Access MAILHOG [localhost:8025/]
8. Access flower [localhost:5555]

## Contributing

Contributions are welcome! Please open an issue or pull request to discuss any changes or improvements.

## License

This project is licensed under the [MIT License] License. 

    
    

    
