from flask import render_template, request, redirect, url_for, Response, flash
from flask.ext.login import login_required, login_user, logout_user, current_user

from btray import app, db
from btray.models import WebhookConfig
from btray.forms import LoginForm
from btray.forms import WebhookConfigForm
from btray.forms import WebhookConfigDeleteForm
from btray.forms import WebhookConfigClearForm


## Pre Handlers
####################################################################
@app.before_request
def before_request():
    if request.url.startswith('http://') and app.config['ENVIRONMENT'] == "production":
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)

## Public App Routes
####################################################################
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('configs_list'))
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)

        flash('Logged in successfully.')

        return redirect(url_for('configs_list'))
    return render_template('login.html', form=form)

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/endpoints/<webhook_config_unique_id>/', methods=['POST'])
def webhook_receiver(webhook_config_unique_id):
    config = WebhookConfig.get_by_unique_id(webhook_config_unique_id)
    if config is None: return Response(status=404)

    webhook_response = config.parse_webhook_response(
        raw=request.form['bt_payload'],
        signature=str(request.form['bt_signature'])
    )

    if webhook_response is not None:
        db.session.commit()
        return Response(status=200)

    return Response(status=500)

## Private App Routes
####################################################################
@app.route("/faq/")
def show_faq():
    return render_template('faq.html')

@app.route('/configs/')
@login_required
def configs_list():
    return render_template('configs_list.html')

@app.route('/configs/<int:webhook_config_id>/')
@login_required
def configs_show(webhook_config_id):
    config = WebhookConfig.get(webhook_config_id, current_user)
    form = WebhookConfigDeleteForm(
        webhook_config_id=webhook_config_id,
        user=current_user
    )
    if config is None:
        return Response(status=404)
    return render_template(
        'configs_show.html',
        config=config,
        clear_form=form
    )

@app.route('/configs/new', methods=['POST','GET'])
@login_required
def configs_new():
    form = WebhookConfigForm(user=current_user)
    if form.validate_on_submit() and form.webhook_config.webhook_config_id is not None:
        return redirect(url_for(
            'webhook_helper',
            webhook_config_unique_id=form.webhook_config.unique_id
        ))
    return render_template('configs_new.html', form=form)

@app.route('/configs/<int:webhook_config_id>/clear', methods=['POST'])
@login_required
def configs_clear(webhook_config_id):
    form = WebhookConfigClearForm(
        webhook_config_id=webhook_config_id,
        user=current_user
    )
    if form.validate_on_submit():
        form.webhook_config.clear()
    return redirect(url_for('configs_show', webhook_config_id=webhook_config_id))

@app.route('/configs/<int:webhook_config_id>/delete', methods=['POST','GET'])
@login_required
def configs_delete(webhook_config_id):
    form = WebhookConfigDeleteForm(
        webhook_config_id=webhook_config_id,
        user=current_user
    )

    if form.validate_on_submit():
        WebhookConfig.delete(form.webhook_config)
        return redirect(url_for('configs_list'))
    return render_template('configs_delete.html', form=form)

@app.route('/endpoints/<webhook_config_unique_id>/', methods=['GET'])
@login_required
def webhook_helper(webhook_config_unique_id):
    config = WebhookConfig.get_by_unique_id(webhook_config_unique_id)
    if config is None: return Response(status=404)

    return render_template('endpoint_helper.html', webhook=config)
