from btray import db
from btray.models.webhook_config import WebhookConfig

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.PasswordType(schemes=['pbkdf2_sha512']), nullable=False)

    webhook_configs = db.relationship('WebhookConfig', backref='user', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.is_active = True

    def __repr__(self):
        return '<user %r>' % self.username

    def is_active(self):
        return self.is_active

    def get_id(self):
        return str(self.user_id)

    def add_webhook_config(self, webhook):
        self.webhook_configs.append(webhook)
        db.session.commit()
        return webhook

    @staticmethod
    def is_authenticated():
        return True

    @classmethod
    def get(cls, user_id):
        return User.query.filter_by(user_id=user_id).first()

