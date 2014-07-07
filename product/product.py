# coding= utf-8


from osv import osv, fields


class product_template(osv.osv):
    _inherit = 'product.template'

    _columns = {
        'type': fields.selection([('service', 'Service'), ('product', 'Producto')], required=True)
    }

    _defaults = {
        'type': 'service'
    }


product_template()
