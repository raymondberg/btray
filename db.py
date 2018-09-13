from btray import db, app
from btray.models import User, WebhookConfig, WebhookResponse

from random import sample as sample
import sys
from getpass import getpass


VALID_COMMANDS = [
    "install",
    "reset",
    "drop",
    "adduser",
    "generate",
    "resetpw",
]

def usage_and_quit():
    print("Usage: python db.py [{}]".format(" | ".join(VALID_COMMANDS)))
    exit()

if len(sys.argv) != 2:
    usage_and_quit()

command = sys.argv[1]
print "Received command: {}".format(command)

if command not in VALID_COMMANDS:
    usage_and_quit()

if command in ["reset","drop"]:
    db.drop_all()
    print("Database cleaned")

if command in ["reset","install"]:
    db.create_all()
    print("Database initialized")

if command == "adduser":
    username = input("Username: ")
    email = input("Email: ")
    password = getpass("Password: ")
    db.session.add(User(username,email,password))

if command == "resetpw":
    username = input("Username: ")
    db.session.query(User).filter(User.username == username).update({'password': getpass("Password: ")})

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
            bt_merchant_id="abc{}".format(i),
            bt_public_key="def{}".format(i),
            bt_private_key="ghi{}".format(i)
        )
        user.webhook_configs.append(webhook_config)

        for j in range(0, 15):
            webhook_config.parse_webhook_response('VGhpcyBpcyBhIHRlc3QNClRoaXMgaXMgb25seSBhIHRlc3QNCklmIHlvdSB0cnkgYW55dGhpbmcgZnVubnkgaXQgd2lsbCBlbmQgcG9vcmx5Lg==','fake-valid-signature-for-testing')
    db.session.add(user)

db.session.commit()
print("Committed")
