from odoo import models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _get_pivot_field_names(self):
        fields = super()._get_pivot_field_names()
        if 'amount_currency' not in fields:
            fields.append('amount_currency')
        return fields