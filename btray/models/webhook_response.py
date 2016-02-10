import base64
import datetime
import pytz

from btray import db

class WebhookResponse(db.Model):
    webhook_response_id = db.Column(db.Integer, primary_key=True)
    raw = db.Column(db.Text, nullable=False)
    signature = db.Column(db.Text, nullable=False)
    xml = db.Column(db.Text)
    parsed = db.Column(db.Text)
    received_at = db.Column(db.DateTime)
    kind = db.Column(db.String("25"), nullable=False)

    fk_webhook_config_id = db.Column(db.Integer, db.ForeignKey('webhook_config.webhook_config_id'), nullable=False)

    def __init__(self, raw, signature, parsed_object):
        self.raw = raw
        self.signature = signature
        self.xml = self._payload_to_xml(raw)
        self.parsed = str(parsed_object)
        self.received_at = datetime.datetime.now(tz=pytz.timezone("UTC"))
        try:
            self.kind = parsed_object.kind
        except Exception:
            self.kind = 'unknown'

    @staticmethod
    def _payload_to_xml(payload):
        return base64.b64decode(payload).decode('utf-8').replace('\\n', '\n')
