from btray import db
from btray.models import User, WebhookConfig, WebhookResponse

import sys
from getpass import getpass

def usage_and_quit():
    print "Usage: python db.py [install | reset | drop | adduser]"
    exit()

if len(sys.argv) != 2:
    usage_and_quit()

command = sys.argv[1]
print "Received command: %s" % command

if command not in ["install", "reset","drop","adduser"]:
    usage_and_quit()

if command in ["reset","drop"]:
    db.drop_all()
    print("Database cleaned")

if command in ["reset","install"]:
    db.create_all()
    print("Database initialized")

if command == "adduser":
    username = raw_input("Username: ")
    email = raw_input("Email: ")
    password = getpass("Password: ")
    db.session.add(User(username,email,password))

db.session.commit()
print("Committed")

