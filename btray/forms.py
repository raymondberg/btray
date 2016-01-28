from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField, validators

from btray.models import User

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
