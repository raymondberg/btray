from flask_wtf import Form
from wtforms import BooleanField
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms import TextField
from wtforms import validators, ValidationError
from sqlalchemy.exc import IntegrityError

from btray.models import User, WebhookConfig

import re

class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    submit = SubmitField('Login')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(username=self.username.data).first()

        if user is None or user.password != self.password.data:
            self.username.errors.append('Unknown username/password')
            return False

        self.user = user
        return True

class SignUpForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    email = TextField('Email', [validators.DataRequired(), validators.Email()])
    submit = SubmitField('Sign Up')

    def validate(self):
        if not Form.validate(self):
            return False

        user = User.query.filter_by(username=self.username.data).first()

        if user is not None:
            self.username.errors.append('username already taken')
            return False

        return True

class WebhookConfigForm(Form):
    name = TextField(
        'Webhook Name',
        [
            validators.Required(),
            validators.Regexp(re.compile('^[a-zA-Z0-9./_ -]+$'),
                message='Only letters,numbers and select special chars allowed (./_-).'),
        ]
    )
    notes = TextAreaField(
        'Webhook Description',
        [
            validators.Required(),
            validators.Regexp(re.compile('^[a-zA-Z0-9./_ -]+$'),
                message='Only letters,numbers and select special chars allowed (./_-).'),
        ]
    )
    bt_merchant_id = TextField(
        'Braintree Merchant ID',
        [
            validators.Required(),
            validators.Regexp(re.compile('^[a-zA-Z0-9]+$')),
        ]
    )
    bt_public_key = TextField(
        'Braintree Public Key',
        [
            validators.Required(),
            validators.Regexp(re.compile('^[a-zA-Z0-9]+$')),
        ]
    )
    bt_private_key = TextField(
        'Braintree Private Key',
        [
            validators.Required(),
            validators.Regexp(re.compile('^[a-zA-Z0-9]+$')),
        ]
    )

    is_sandbox = BooleanField(
        'I affirm that these credentials are SANDBOX credentials',
        [
            validators.Required(),
            validators.AnyOf([True]),
        ]
    )

    is_mine = BooleanField(
        'I have personally disabled every single permission' + '<br>' +
        'for these credentials(e.g. Webhook Only Role)',
        [
            validators.Required(),
            validators.AnyOf([True]),
        ]
    )

    submit = SubmitField('Create Webhook Config')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = kwargs['user']

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        try:
            self.webhook_config = self.user.add_webhook_config(WebhookConfig(
                name=self.name.data,
                notes=self.notes.data,
                bt_merchant_id=self.bt_merchant_id.data,
                bt_public_key=self.bt_public_key.data,
                bt_private_key=self.bt_private_key.data,
            ))
        except IntegrityError as error:
            self.bt_public_key.errors.append("A webhook endpoint with this public key already exists")
            return False

        return True

class WebhookConfigDeleteForm(Form):
    webhook_config_id = HiddenField('WebhookConfigID', [validators.Required()])
    submit = SubmitField('Yes, I promise you can delete it')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

        self.url_config_id = kwargs['webhook_config_id']
        self.webhook_config = WebhookConfig.get(self.url_config_id, kwargs['user'])

class WebhookConfigClearForm(Form):
    webhook_config_id = HiddenField('WebhookConfigID', [validators.Required()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

        self.url_config_id = kwargs['webhook_config_id']
        self.webhook_config = WebhookConfig.get(self.url_config_id, kwargs['user'])
