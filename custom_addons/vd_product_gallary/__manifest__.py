
{
    'name': 'Product Gallery',
    'version': '18.0.1.6',
    'sequence': 1,
    'category': 'Generic Modules/Tools',
    'description':
        """
        This Module add below functionality into odoo

        -Product Gallery\n

    """,
    'summary': 'Product Gallery',
    'author': 'Vishal Designer',
    'website': 'http://www.devintellecs.com',
    'depends': ['base','product','web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'data/sequence.xml',
        'data/product_demo.xml',
        'views/main_menu.xml',
      #  'wizard/create_task.xml',
        'wizard/whatsapp.xml',
        'views/video_gallary.xml',
        'views/category_view.xml',
        'views/product.xml',
        # Dashboard
        'views/dashboard_menu.xml',
        'wizard/product_cust_history.xml',
    ],

      'assets': {
         'web.assets_backend': [
       'vd_product_gallary/static/src/css/dashboard_new.css',
       'vd_product_gallary/static/src/js/chart_chart.js',
       'vd_product_gallary/static/src/js/product_gallary_dashboard.js',
       'vd_product_gallary/static/src/xml/product_gallary_dashboard_template.xml',
   ],
    },
    

    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
