# -*- coding: utf-8 -*-
# Part of Godo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Italy - E-invoicing',
    'icon': '/l10n_it/static/description/icon.png',
    'version': '0.3',
    'depends': [
        'l10n_it',
        'fetchmail',
        'account_edi'
    ],
    'author': 'Godo',
    'description': """
E-invoice implementation
    """,
    'category': 'Accounting/Localizations/EDI',
    'website': 'http://smartlifevn.com/',
    'data': [
        'security/ir.model.access.csv',
        'data/account_edi_data.xml',
        'data/invoice_it_template.xml',
        'data/invoice_it_simplified_template.xml',
        'views/l10n_it_view.xml',
        ],
    'demo': [
        'data/account_invoice_demo.xml',
    ],
    'license': 'LGPL-3',
}
