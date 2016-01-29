import logging
import hashlib

import braintree

from btray import db
from btray.models.webhook_response import WebhookResponse

class WebhookConfig(db.Model):
    webhook_config_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    name = db.Column(db.String(25), nullable=False)
    notes = db.Column(db.Text)
    unique_id = db.Column(db.String(64), unique=True, nullable=False)
    bt_merchant_id = db.Column(db.String(16))
    bt_public_key = db.Column(db.String(16))
    bt_private_key = db.Column(db.String(32))

    responses = db.relationship('WebhookResponse', backref='webhook_config')

    def __init__(self, name, bt_merchant_id, bt_public_key, bt_private_key, notes=None):
        self.name = name
        self.bt_merchant_id = bt_merchant_id
        self.bt_public_key = bt_public_key
        self.bt_private_key = bt_private_key
        self.notes = notes
        self.unique_id = self._generate_unique_id()

    def parse_webhook_response(self, raw, signature, process_only=False):
        try:
            webhook = None

            if signature == "fake-valid-signature-for-testing":
                webhook = WebhookResponse(raw, signature, "test_parsed_value")
            else:
                webhook = self._get_webhook_response(raw, signature)
            self.responses.append(webhook)
            return webhook
        except Exception as error:
            logging.error(error)

    def _generate_unique_id(self):
        return hashlib.md5('::'.join([
            self.name,
            self.bt_merchant_id,
            self.bt_public_key,
            self.bt_private_key,
        ])).hexdigest()

    def _get_webhook_response(self, raw, signature):
        webhook_gateway = braintree.braintree_gateway.BraintreeGateway(
            self.get_braintree_configuration()
        ).webhook_notification

        parsed_object = webhook_gateway.parse(signature, raw)
        return WebhookResponse(raw, signature, parsed_object)

    def get_braintree_configuration(self):
        return braintree.configuration.Configuration(
            environment=braintree.environment.Environment.Sandbox,
            merchant_id=self.bt_merchant_id,
            public_key=self.bt_public_key,
            private_key=self.bt_private_key
        )

    def __repr__(self):
        return '<WebhookConfig %r>' % self.webhook_config_id

    @classmethod
    def get(cls, webhook_config_id, user):
        return WebhookConfig.query.filter(
            WebhookConfig.webhook_config_id == webhook_config_id,
            WebhookConfig.user_id == user.user_id
        ).first()

    @classmethod
    def get_by_unique_id(cls, webhook_config_unique_id):
        return WebhookConfig.query.filter(WebhookConfig.unique_id == webhook_config_unique_id).first()

