from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    company_currency_id2 = fields.Many2one(string='Second Company Currency', related='company_id.currency_id2', readonly=True, store=True)
    conversion_rate = fields.Float(string='Conversion Rate', store=True, tracking=True)
    custom_rate = fields.Float(string='Custom Rate', default=-1, tracking=True)
    debit2 = fields.Monetary(string='Debit2', currency_field='company_currency_id2', default=0, store=True, tracking=True)
    credit2 = fields.Monetary(string='Credit2', currency_field='company_currency_id2', default=0, store=True, tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if records:
            records.with_context(skip_currency_recalc=True)._update_currency_values()
        return records

    def write(self, vals):
        result = super().write(vals)
        if not self.env.context.get('skip_currency_recalc') and any(
            field in vals for field in ['debit', 'credit', 'amount_currency', 'currency_id', 'custom_rate', 'conversion_rate', 'move_id']
        ):
            self.with_context(skip_currency_recalc=True)._update_currency_values(vals.get('conversion_rate'))
        return result

    @api.onchange('debit', 'credit', 'amount_currency', 'currency_id', 'custom_rate', 'conversion_rate', 'move_id')
    def _onchange_currency_fields(self):
        self._update_currency_values()

    def _update_currency_values(self, manual_conversion_rate=None):
        values_by_record = {}
        for rec in self:
            values = {}
            if manual_conversion_rate is not None:
                values['conversion_rate'] = manual_conversion_rate
                values['custom_rate'] = manual_conversion_rate
                values['debit2'] = rec.debit / manual_conversion_rate if manual_conversion_rate else 0
                values['credit2'] = rec.credit / manual_conversion_rate if manual_conversion_rate else 0
            elif rec.custom_rate == -1:
                conversion_rate = 1
                main_currency = self.env.company.currency_id
                to_currency = self.env.company.currency_id2
                date = rec.move_id.invoice_date or rec.move_id.date

                if rec.debit and rec.company_currency_id2 and rec.currency_id and (rec.move_id.invoice_date or rec.move_id.date):
                    from_currency = rec.currency_id
                    if rec.amount_currency:
                        if from_currency.id == to_currency.id:
                            conversion_rate = rec.debit / abs(rec.amount_currency) if abs(rec.amount_currency) else 1
                            values['debit2'] = abs(rec.amount_currency)
                        else:
                            conversion_rate = self._get_rate(to_currency, main_currency, rec, date)
                            values['debit2'] = rec.debit / conversion_rate if conversion_rate else 0
                    else:
                        if main_currency.id == to_currency.id:
                            conversion_rate = 1
                            values['debit2'] = rec.debit
                        else:
                            conversion_rate = self._get_rate(to_currency, main_currency, rec, date)
                            values['debit2'] = rec.debit / conversion_rate if conversion_rate else 0
                    values['conversion_rate'] = conversion_rate

                if rec.credit and rec.company_currency_id2 and rec.currency_id and (rec.move_id.invoice_date or rec.move_id.date):
                    from_currency = rec.currency_id
                    if rec.amount_currency:
                        if from_currency.id == to_currency.id:
                            conversion_rate = rec.credit / abs(rec.amount_currency) if abs(rec.amount_currency) else 1
                            values['credit2'] = abs(rec.amount_currency)
                        else:
                            conversion_rate = self._get_rate(to_currency, main_currency, rec, date)
                            values['credit2'] = rec.credit / conversion_rate if conversion_rate else 0
                    else:
                        if main_currency.id == to_currency.id:
                            conversion_rate = 1
                            values['credit2'] = rec.credit
                        else:
                            conversion_rate = self._get_rate(to_currency, main_currency, rec, date)
                            values['credit2'] = rec.credit / conversion_rate if conversion_rate else 0
                    values['conversion_rate'] = conversion_rate
            else:
                values['conversion_rate'] = rec.custom_rate
                values['credit2'] = rec.credit / rec.custom_rate if rec.custom_rate else 0
                values['debit2'] = rec.debit / rec.custom_rate if rec.custom_rate else 0

            if values:
                values_by_record[rec.id] = values

        if values_by_record:
            for record_id, values in values_by_record.items():
                self.browse(record_id).with_context(skip_currency_recalc=True).write(values)

    def _get_rate(self, to_currency, main_currency, rec, date):
        if rec.move_id.asset_id:
            return self.env['res.currency']._get_conversion_rate(
                to_currency,
                main_currency,
                self.env.company,
                rec.move_id.asset_id.acquisition_date,
            )
        return self.env['res.currency']._get_conversion_rate(
            to_currency,
            main_currency,
            self.env.company,
            date,
        )

