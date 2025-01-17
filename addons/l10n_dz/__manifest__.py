# -*- coding: utf-8 -*-
# Part of Godo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Algeria - Accounting',
    'version': '1.0',
    'category': 'Accounting/Localizations/Account Charts',
    'description': """
This is the module to manage the accounting chart for Algeria in Godo.
======================================================================
This module applies to companies based in Algeria.
""",
    'author': 'Osis',
    'depends': ['account'],
    'data': [
        'data/account_chart_template_data.xml',
        'data/account.account.template.csv',
        'data/account_chart_template_post_data.xml',
        'data/account_tax_data.xml',
        'data/account_fiscal_position_template_data.xml',
        'data/account_chart_template_configuration_data.xml',
    ],
    'license': 'LGPL-3',
}
