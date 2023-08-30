from . import models

from odoo import api, SUPERUSER_ID


def _uninstall_reset_changes(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['web_editor.assets'].reset_asset(
        '/poc_web_theme/static/src/colors.scss', 
        'web._assets_primary_variables'
    )