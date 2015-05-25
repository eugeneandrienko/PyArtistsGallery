"""Views for service pages.

Special pages with service functions. List of pages:
 * page, which shows on the first run of application --
implemented by first_run() function.
 * update page - implements by update_application().
"""

from jinja2 import TemplateNotFound
from flask import render_template, abort, request, \
    redirect, url_for
from sqlalchemy.exc import OperationalError

from pagapp.support_functions import flash_form_errors, is_first_run
from pagapp.database_functions import create_database
from pagapp.service_pages import service_pages
from pagapp.service_pages.forms import FirstRunForm
from pagapp.models import db
from pagapp.models.users import Users
from pagapp.models.configuration import Configuration


@service_pages.route('/first_run', methods=['GET', 'POST'])
def first_run():
    """Renders service page on the first run."""
    if is_first_run() is False:
        return redirect(url_for('public_pages.index'))
    else:
        create_database()

    form = FirstRunForm()

    # Add data from existing tables to form.
    try:
        form.gallery_title.data = Configuration.query.first().gallery_title
    except (OperationalError, AttributeError):
        pass
    try:
        form.username.data = Users.query.first().nickname
    except (OperationalError, AttributeError):
        pass

    if request.method == 'POST' and form.validate():
        try:
            Configuration.query.first().gallery_title = form.gallery_title.data
        except AttributeError:
            new_configuration = Configuration(form.gallery_title.data)
            db.session.add(new_configuration)

        try:
            Users.query.first().nickname = form.username.data
            Users.query.first().set_new_password(form.password.data)
        except AttributeError:
            new_administrator = Users(
                form.username.data, form.password.data, True)
            db.session.add(new_administrator)

        db.session.commit()
        return redirect(url_for('public_pages.index'))
    else:
        flash_form_errors(form)

    try:
        return render_template('first_run.html', form=form)
    except TemplateNotFound:
        abort(404)