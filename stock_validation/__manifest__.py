{
    'name': "Stock Validation",

    'summary': """Se valida la cantidad disponible en la ubicacion de destino""",

    'author': "Tonny Velazquez",
    'website': "corner.store59@gmail.com",

    'category': 'Stock',
    'version': '15.0.0.0.1',

    'depends': ['stock', 'stock_analytic'],

    'data': [
        'views/stock_picking_views.xml',
    ],
}
