# btray
Tool for reviewing Braintree webhooks.

## Installation

To setup, copy the `configuration.py.sample` file to `configuration.py` and edit values as needed. At the very least, be sure to change your `SECRET_KEY` value.

Next install the requirements by running `pip install -r requirements.txt`.

Follow this by setting up the database `python db.py install`. If you want to seed the database in dev with a sample user, run `python db.py generate`.

Now you're ready to run the app! Just run `python run.py` to start the Flask server.

## Databases

The app is configured to use sqlite in dev for portability, but to install with mysql in prod just add the following to your requirements file and uncomment the MySQL settings.
```
MySQL-python==1.2.5
```

## Developing Locally

To get setup run:

```
cp docker.env.sample docker.env

# Before you go forward, update the docker.env POSTGRES_PASSWORD and SECRET_KEY

docker-compose build
docker-compose up
docker exec -it webhooket-db psql -U postgres -c "create database webhooket;"
docker exec -it webhooket python db.py install
docker exec -it webhooket python db.py adduser
```

To open a shell for testing or other purposes, run this:

```
docker exec -it webhooket bash
```

# CAUTION

This project is intended to be used at ones own risk. The author(s) accept no responsibility should you be so foolish as to turn this product on somewhere.
