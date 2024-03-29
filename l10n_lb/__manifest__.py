# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Main contributor: Wafi Chaar. HLOUL-BAS
# Copyright (C) 2019 HLOUL-BAS (<http://www.hloul-bas.com>) 

{
    'name': "Lebanon - Accounting",
    'version': '16.0',
    'author': 'BAS',
    'website': 'http://www.bas.sarl',
    'category': 'Localization',
    'license': 'AGPL-3',	
    'description': """
Lebanon - Accounting localization: 
chart of accounts, tax and stock valuation
by BAS
==========================================
    """,

    'depends': ['account'],

    'data': [
        'data/l10n_lb_data.xml',
        'data/l10n_lb_chart_data.xml',
        'data/account.account.template.csv',
        'data/account_tax_group_data.xml',
        'data/l10n_lb_chart_post_data.xml',
        'data/account_tax_template_data.xml',
        'data/account_chart_template_data.xml',
    ],

}
