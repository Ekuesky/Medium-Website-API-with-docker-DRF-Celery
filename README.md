TODO:rewrite this readme
# apipro

This project provides a professional structure for building a Django REST API with Docker. It includes features such as user authentication, profiles, and basic CRUD operations.

## Features

* **User Authentication:**  Allows users to register, login, and manage their accounts.
* **Profiles:** Users can create and update their own profile details.
* **Articles:** Users can create, rate, update, delete article
* **Following:** Users can follow each other.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ekuesky/apipro.git

2. Install dependencies:   
    cd apipro
    pip install -r requirements/local_req.txt
3. Configure database:
    Create a database for your project.
    Update database connection settings in apipro/settings/local.py.

4. Run migrations:      
    python manage.py makemigrations
    python manage.py migrate
   
5. Create a superuser:
    python manage.py createsuperuser

6. Start the development server:
    python manage.py runserver

   ENJOY
   **AYIEK**

    
    

    
