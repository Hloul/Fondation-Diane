from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    company_currency_id2 = fields.Many2one(string='Second Company Currency', related='company_id.currency_id2', readonly=True, store=True)
    conversion_rate = fields.Float(
        string='Conversion Rate',
        compute='_compute_conversion_rate',
        inverse='_inverse_conversion_rate',
        store=True,
        tracking=True,
    )
    custom_rate = fields.Float(string='Custom Rate', default=-1, tracking=True)
    debit2 = fields.Monetary(string='Debit2', currency_field='company_currency_id2', default=0, tracking=True)
    credit2 = fields.Monetary(string='Credit2', currency_field='company_currency_id2', default=0, tracking=True)

    @api.depends('amount_currency','date','currency_id','debit','credit','custom_rate')
    def _compute_conversion_rate(self):
        for rec in self:
          if rec.custom_rate == -1:
            conversion_rate = 1
            main_currency = self.env.company.currency_id
            to_currency = self.env.company.currency_id2
            date = rec.move_id.invoice_date or rec.move_id.date
            if rec.debit and rec.company_currency_id2 and rec.currency_id and (rec.move_id.invoice_date or rec.move_id.date):
                from_currency = rec.currency_id
                if rec.amount_currency:
                    if from_currency.id == to_currency.id:
                        conversion_rate = rec.debit / abs(rec.amount_currency)
                        rec.debit2 = abs(rec.amount_currency)
                    else:
                        if rec.move_id.asset_id:
                            conversion_rate = self.env['res.currency']._get_conversion_rate(
                                to_currency, main_currency, self.env.company, rec.move_id.asset_id.acquisition_date
                            )
                        else:
                            conversion_rate = self.env['res.currency']._get_conversion_rate(
                                to_currency, main_currency, self.env.company, date
                            )
                        rec.debit2 = rec.debit / conversion_rate
                else:
                    # Line in company currency
                    if main_currency.id == to_currency.id:
                        conversion_rate = 1
                        rec.debit2 = rec.debit
                    else:
                        if rec.move_id.asset_id:
                            conversion_rate = self.env['res.currency']._get_conversion_rate(
                                to_currency, main_currency, self.env.company, rec.move_id.asset_id.acquisition_date
                            )
                        else:
                            conversion_rate = self.env['res.currency']._get_conversion_rate(
                                to_currency, main_currency, self.env.company, date
                            )
                        rec.debit2 = rec.debit / conversion_rate
                rec.conversion_rate = conversion_rate
            if rec.credit and rec.company_currency_id2 and rec.currency_id and (rec.move_id.invoice_date or rec.move_id.date):
                from_currency = rec.currency_id
                if rec.amount_currency:
                    if from_currency.id == to_currency.id:
                        conversion_rate = rec.credit / abs(rec.amount_currency)
                        rec.credit2 = abs(rec.amount_currency)
                    else:
                        if rec.move_id.asset_id:
                            conversion_rate = self.env['res.currency']._get_conversion_rate(
                                to_currency, main_currency, self.env.company, rec.move_id.asset_id.acquisition_date
                            )
                        else:
                            conversion_rate = self.env['res.currency']._get_conversion_rate(
                                to_currency, main_currency, self.env.company, date
                            )
                        rec.credit2 = rec.credit / conversion_rate
                else:
                    # Line in company currency
                    if main_currency.id == to_currency.id:
                        conversion_rate = 1
                        rec.credit2 = rec.credit
                    else:
                        if rec.move_id.asset_id:
                            conversion_rate = self.env['res.currency']._get_conversion_rate(
                                to_currency, main_currency, self.env.company, rec.move_id.asset_id.acquisition_date
                            )
                        else:
                            conversion_rate = self.env['res.currency']._get_conversion_rate(
                                to_currency, main_currency, self.env.company, date
                            )
                        rec.credit2 = rec.credit / conversion_rate
                rec.conversion_rate = conversion_rate
          else:
            rec.conversion_rate = rec.custom_rate   
            rec.credit2 = rec.credit / rec.conversion_rate if rec.conversion_rate else 0
            rec.debit2 = rec.debit / rec.conversion_rate if rec.conversion_rate else 0

 


    def _inverse_conversion_rate(self):
        for rec in self:
          if rec.conversion_rate:
            rec.debit2 = rec.debit / rec.conversion_rate
            rec.credit2 = rec.credit / rec.conversion_rate
          rec.custom_rate = rec.conversion_rate
          

          

