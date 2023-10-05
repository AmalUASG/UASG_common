# -*- coding: utf-8 -*-
{
    'name': "uasg_single_sign_on",

    'summary': """
        This module is providing the single sign on feature         

""",

    'description': """
       The single sign on feature , to allow users to sign in only using their Azure account credentials 
    """,

    'author': "UASG",
    'website': "https://www.alsaqergroup.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base' ,'auth_oauth'],

    # always loaded
    'data': [
      
        # 'views/template.xml',
        'data/data.xml'
 
    ], 
}
