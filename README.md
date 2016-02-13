# btray
Tool for reviewing Braintree webhooks.

## Installation

To setup, copy the `configuration.py.sample` file to `configuration.py` and edit values as needed. At the very least, be sure to change your `SECRET_KEY` value.

Next install the requirements by running `pip install -r requirements.txt`.

Follow this by setting up the database `python db.py install`. If you want to seed the database in dev with a sample user, run `python db.py generate`.

Now you're ready to run the app! Just run `python run.py` to start the Flask server.

# CAUTION

This project is intended to be used at ones own risk. The author(s) accept no responsibility should you be so foolish as to turn this product on somewhere.
