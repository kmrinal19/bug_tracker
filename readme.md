# Bug Tracker
Bug Tracker is an app that aids in tracking bugs, issues, and questions in any app development. It provides a collaborative environment for the team to solve the issues related to the project. Currently only IMG members can sign in using omniport.

<b>Built with</b>
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)

## Setup
- Prerequisites:
  - Python 3
  - pip
  - MySql
  - Docker

- Clone this repository.

- Set up a virtual environment.
```
python3 -m venv bug_tracker_env
```

- Activate the virtual environment.
```
source bug_tracker_env/bin/activate
```

- Create a MySql database named bugDB.

- Navigate inside the cloned repository and install the required dependencies using the command:
```
pip install -r requirements.txt
```

- Navigate to /bug_tracker and create a file .env and store the following credentials inside it
```
SECRET_KEY=your-secret-key

DATABASE_PASSWORD=mysql-database-password

EMAIL_ID=gmail-id-for-smtp
EMAIL_PASSWORD=password-for-gmail-id

CLIENT_ID=omniport-oauth-client-id
CLIENT_SECRET=omniport-oauth-client-secret
```

- Navigate back to the base directory for the app where <span>manage.py</span> file is located and make the database migrations using following command:
```
python manage.py makemigrations
python manage.py migrate
```

- Start a Redis server on port 6379 using the following command:
```
docker run -p 6379:6379 -d redis:5
```

- Start the backend server:
```
python mange.py runserver
```