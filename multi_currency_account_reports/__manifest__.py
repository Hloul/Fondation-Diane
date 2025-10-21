# -*- coding: utf-8 -*-
{
    'name': "Multi-Currency Accounting Reports",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'account_reports'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/trial_balance.xml',
        'data/general_ledger_multi_currency.xml',
        'data/partner_ledger_multi_currency.xml',
        'data/account_report_actions.xml',
        'data/menuitems.xml',
        'views/res_company.xml',
        'views/account_move.xml',
        'views/account_move_line.xml',
    ],
}
