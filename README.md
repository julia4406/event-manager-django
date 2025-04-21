# Event Manager / Django REST Framework

**A Django-based REST-Api that manages events (such as conferences, meetups, etc.
).**
This application allows users to create, view, update, and delete events.
It also handles user registration and cancellation for events.

**Tech Stack:** 
- **Backend:** Django REST Framework.
- **Containerization:** Docker & Docker Compose.
- **Dependency Management:** Poetry.


## What's inside:
- Basic User Registration and Authentication.
- Event Registration/Cancellation
- Search and filtering
- API documentation (Swagger)
- Dockerized setup for easy deployment

## API Endpoints
**Authentication is required to access these endpoints.**

### Event Endpoints


| Method        | Endpoint                           | Description                                                                                                   |
|---------------|------------------------------------|---------------------------------------------------------------------------------------------------------------|
| `GET`         | `/event/events/`                   | List all events with optional filtering, <br/>searching, and sorting. <br/>Available for all authenticated users |
| `POST`        | `/event/events/`                   | Creation of a new event.                                                                                      |
| `GET`         | `/event/events/{id}/`              | Retrieve details for a specific event by its ID.                                                              |
| `PUT/PATCH`   | `/event/events/{id}/`              | Update event details.<br/> Only owner(organizer) or admin allowed to change the event.                        |
| `DELETE`      | `/event/events/{id}/`              | Delete an event (By admin or organizer only)                                                                  |
| `POST`        | `/event/events/{id}/register/`     | Register for an event. <br/>The currently authenticated user can register for a specific event.               |
| `POST`        | `/event/events/{id}/unregister/`   | Cancel registration for an vent                                                                               |


### User Profile Endpoints

These endpoints available for current authenticated user. Allow to view 
information about profile and events associated with this user.

| Method      | Endpoint                               | Description                                                                                                                                                   |
|-------------|----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `GET`       | `/user/profile/`                       | Retrieve profile information.                                                                                                                                 |
| `PUT/PATCH` | `/user/profile/`                       | Update profile information.                                                                                                                                   |
| `GET`       | `/user/profile/organized-events/`      | List events the user is attending.<br/>Retrieves events where the current user is a participant.<br/>Filter, search and sorting by event available.           |
| `GET`       | `/user/profile/participated-events/`   | List events the user is attending.<br/>Retrieves events events organized by currently authenticated user.<br/>Filter, search and sorting by event available.  |

### Management User Records Endpoints (admin only)
All information about registered users. CRUD operations with profiles, search 
by user (username, email, first and last name).
Only accounts authorized as admin (is_staff=True) can manage these endpoints.

| Method        | Endpoint               | Description                                                                                                                                                               |
|---------------|------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `GET`         | `/user/manage/`        | List all registered users with information <br/>about the events they are registered for or have organized.<br/>Available search by username, email, first and last name. |
| `POST`        | `/user/manage/`        | Admin can create new user account.                                                                                                                                        |
| `GET`         | `/user/manage/{id}/`   | Retrieve details for a specific  user account.                                                                                                                            |
| `PUT/PATCH`   | `/user/manage/{id}/`   | Update details for a specific  user account.                                                                                                             |
| `DELETE`      | `/user/manage/{id}/`   | Delete specific user account.                                                                                                                                             |

### Signup Endpoint

| Method | Endpoint         | Description                                                                                                      |
|--------|------------------|------------------------------------------------------------------------------------------------------------------|
| `POST` | `/user/signup/`  | New user registration. Creates account for the new user.|



## Getting Started
### Installation & Setup

Follow the steps below to set up the project on your local machine:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/julia4406/event-manager-django

2. **Install Dependencies: Use Poetry to install all required dependencies:**
   ```bash
   poetry install
   
3. **Use the `.env.sample` file as a template to create your own `.env` file 
   (simply copy all contents).**  
 - **Note:** These settings are provided for demonstration purposes only. For 
   security reasons, you should replace them with your own environment-specific values.
 - **Note2:** If you are using google - you have to set up EMAIL_HOST_PASSWORD 
 in the security section of your account.
   ```bash
   https://myaccount.google.com/security

4. **Launch the Application: Spin up all services with Docker Compose:**
   ```bash
   docker-compose up --build
   
5. **Application will be available on your local machine. Enter in browser:**

- to register new user
    ```bash
    http://127.0.0.1:8000/user/signup/
- documentation (you can see list of all endpoints)
   ```bash
   http://127.0.0.1:8000/api/doc/swagger/
   
- events endpoints
   ```bash
    http://127.0.0.1:8000/event/

6. **Configuration:**
  - Configure environment variables as needed.
  - Review the pyproject.toml for dependency configurations.

7. **Django admin panel:**
You can create superuser to have access to django admin panel
  - Enter into docker container:
    ```bash
    docker exec -it event_manager_web sh
  - Enter command to create superuser
    ```bash
    python src/manage.py createsuperuser
  - follow instructions in terminal
  - After creating you can enter to admin-panel with created credentials
    ```bash
    http://127.0.0.1:8000/admin
