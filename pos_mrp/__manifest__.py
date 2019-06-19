# -*- coding: utf-8 -*-
{
    'name': "Generate MO with the POS",

    'summary': """
       Generate MO for MTO and Product product sell with the POS""",

    'description': """
       
    """,

    'author': "Thibault Francois",
    'website': "https://github.com/tfrancoi/pos_mrp",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Point of Sale',
    'version': '1.0',

    # any module necessary for this one to work correctly
    # Could be changed if necessary
    'depends': [ 'point_of_sale',  'mrp', 'stock'],

    # always loaded
    'data': [
       
    ],
    'installable': True,
}
