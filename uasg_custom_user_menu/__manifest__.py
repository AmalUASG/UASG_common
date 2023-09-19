# -*- coding: utf-8 -*-
{
    'name': "UASG Customize Menu",

    'summary': """
        This module is providing customization on user Menu         

""",

    'description': """
        This module is providing customization on user Menu         
    """,

    'author': "UASG",
    'website': "https://www.alsaqergroup.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base' ],

    # always loaded
    'data': [
      
        # 'views/template.xml',
 
    ], 

     'assets': {
        'web.assets_backend': [
            'uasg_custom_user_menu/static/src/js/menu.js']}
    

}
