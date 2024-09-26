# "Telegram bot for tracking habits"


The functionality of the application
The main functions of the application on the frontend side (telegram bot):

● Adding and removing habits, full
editing functionality;

● the function of fixing the fulfillment of a habit: fulfilled / not
fulfilled;

● A reminder to follow a habit with
fixation.
The main function of the service script is to notify the user at
a specified/designated time interval.
The main functions of the application on the backend side (FastAPI):

● storage and processing of data received from the user
(requests from the telegram bot);

● Authentication and authorization of the telegram bot to access
data.

## Technology stack:

During the implementation, use the following technology stack:

● Poetry.

● PostgreSQL.

● SQLAlchemy.

● Alembic.

● PytelegramBotAPI.

● FastAPI.

● PyJWT.

● Apscheduler.

● Docker-compose.


## Installation and launch

Make sure that you have Docker and docker-compose installed.


1.Create a private key and a public key using openssl and move it to the certs folder:
```
openssl genrsa -out jwt-private.pem 2048
```

```
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```

2.Create and fill it out.env and db.env

3.Launch ngrok (To access the public internet web server,
application or service running on their local computer)

4.Enter the generated address in .env BACK_URL

5.Building and launching containers with the application and database:
```
docker-compose up
```

## Usage
### Bot commands.
```
/help — help on the bot's commands.

/start — user registration.

/add_habit — information about a new habit.

/habits — getting a list of habits.

/edit_habit — select a habit to edit.

/track_habit — selects a habit to mark the progress.

/habit_stats — statistics of habit fulfillment.

/set_reminder — reminder to mark the completion of habits.

```