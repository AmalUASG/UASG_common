# -*- coding: utf-8 -*-
{
    'name': "UASG Custom eLearning",

    'summary': """
        This module is providing customization on eLearning Module

""",

    'description': """
        This module is providing customization on eLearning Module     
    """,

    'author': "UASG/amal.abdelmajid",
    'website': "https://www.alsaqergroup.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website_slides' ],

    # always loaded
    'data': [
      
        'views/views.xml',
 
    ],    

}
