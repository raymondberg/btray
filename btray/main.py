from btray import app, login_manager
import btray.routes
import btray.models

from flask import render_template

@login_manager.user_loader
def load_user(user_id):
    user = btray.models.User.get(user_id)
    return user

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(401)
def page_restricted(e):
    return render_template('404.html'), 401

application = app
