# -*- coding: utf-8 -*-

{
    'name': 'Punto de venta unido a facturacion electrónica',
    'version': '3.1',
    'category': 'Point of Sale',
    'sequence': 6,
    'summary': 'Punto de venta unido a facturacion electrónica',
    'description': """ Cambios al punto de venta para generar facturas electrónicas fácilmente """,
    'author': 'aquíH',
    'website': 'http://www.aquih.com',
    'depends': ['pos_gt', 'fel_gt'],
    'data': [],
    'installable': True,
    'auto_install': False,
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_fel/static/src/**/*',
        ],
    },
    'license': 'Other OSI approved licence',
}
