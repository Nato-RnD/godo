# -*- coding: utf-8 -*-
# Part of Godo. See LICENSE file for full copyright and licensing details.

# Copyright (c) 2011 Cubic ERP - Teradata SAC. (http://cubicerp.com).

{
    "name": "Panama - Accounting",
    "description": """
Panamenian accounting chart and tax localization.

Plan contable panameño e impuestos de acuerdo a disposiciones vigentes

Con la Colaboración de
- AHMNET CORP http://www.ahmnet.com

    """,
    "author": "Cubic ERP",
    'category': 'Accounting/Localizations/Account Charts',
    "depends": ["account"],
    "data": [
        "data/l10n_pa_chart_data.xml",
        "data/account_tax_group_data.xml",
        "data/account_tax_data.xml",
        "data/account_chart_template_data.xml",
    ],
    'license': 'LGPL-3',
}
