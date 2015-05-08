from jinja2 import TemplateNotFound
from flask import abort, current_app, render_template
from flask import redirect, url_for
from flask_login import logout_user, login_required

from pagapp.admin_panel import admin_panel
from pagapp.admin_panel.admin_functions import change_password
from pagapp.admin_panel.forms import ChangePasswordForm


@admin_panel.route('/logout')
@login_required
def logout():
    """Performs user logout if (s)he go to corresponding URL."""
    logout_user()
    return redirect(url_for('public_pages.index'))


@admin_panel.route('/panel', methods=['GET', 'POST'])
@login_required
def panel():
    panel_forms = {
        'change_password_form': ChangePasswordForm()
    }
    form_controllers = {
        'change_password_form': change_password
    }

    for form in panel_forms:
        try:
            form_controllers[form](
                panel_forms[form]
            )
        except KeyError:
            continue

    try:
        return render_template(
            'panel.html',
            title=current_app.config['GALLERY_TITLE'],
            panel_forms=panel_forms)
    except TemplateNotFound:
        abort(404)