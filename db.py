from btray import db, app
from btray.models import User, WebhookConfig, WebhookResponse

from random import sample as sample
import sys
from getpass import getpass

def usage_and_quit():
    print "Usage: python db.py [install | reset | drop | adduser | generate]"
    exit()

if len(sys.argv) != 2:
    usage_and_quit()

command = sys.argv[1]
print "Received command: %s" % command

if command not in ["install", "reset","drop","adduser", "generate"]:
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

if command == "generate":
    if app.config["ENVIRONMENT"] == "production":
        raise Exception("Cannot generate in production")

    words = ["Horse", "Zenith", "Goose", "Farmer", "Obsidian",
        "Grapefruit", "Martian", "Coal", "Morlock"]

    password = app.config.get("TESTING_USER_PASSWORD", None)
    if password is None:
        password = getpass("Password for 'user': ")

    user = User("user", "user@example.com", password)
    for i in range(0,10):
        webhook_config = WebhookConfig(
            name=" ".join(sample(words, 4)),
            notes="\n".join(sample(words,6)),
            bt_merchant_id="abc%s" % i,
            bt_public_key="def%s" % i,
            bt_private_key="ghi%s" % i
        )
        user.webhook_configs.append(webhook_config)

        for j in range(0, 15):
            webhook_config.parse_webhook_response('VGhpcyBpcyBhIHRlc3QNClRoaXMgaXMgb25seSBhIHRlc3QNCklmIHlvdSB0cnkgYW55dGhpbmcgZnVubnkgaXQgd2lsbCBlbmQgcG9vcmx5Lg==','fake-valid-signature-for-testing')
    db.session.add(user)

db.session.commit()
print("Committed")

