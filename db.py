from btray import db
from btray.models import User, WebhookConfig, WebhookResponse

import sys

def usage_and_quit():
    print "Usage: python db.py [install | reset | drop]"
    exit()

if len(sys.argv) != 2:
    usage_and_quit()

command = sys.argv[1]
print "Received command: %s" % command

if command not in ["install", "reset","drop"]:
    usage_and_quit()

if command in ["reset","drop"]:
    db.drop_all()
    print("Database cleaned")

if command in ["reset","install"]:
    db.create_all()
    print("Database initialized")

db.session.commit()
print("Committed")

