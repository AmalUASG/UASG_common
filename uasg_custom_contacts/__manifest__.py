# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Microsoft Users USAG',
    'category': 'Hidden/Tools',
    'description': """
The module adds Microsoft user in res user.
===========================================
""",
    'depends': ['microsoft_account'],
    'data': [
    'security/ir.model.access.csv',
    'views/ad_configuration.xml',
    'views/uasg_groups.xml'
       
    ],
    'license': 'LGPL-3',
}
