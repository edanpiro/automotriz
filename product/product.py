# coding= utf-8


from osv import osv, fields
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp


class product_template(osv.osv):
    _inherit = 'product.template'

    _columns = {
        'type': fields.selection([('service', 'Service'), ('product', 'Producto')], required=True),
        'standard_price': fields.float('Cost', digits_compute=dp.get_precision('Product Price'), help="Cost price of the product used for standard stock valuation in accounting and used as a base price on purchase orders.", groups="base.group_user"),
    }

    _defaults = {
        'standard_price': 10
    }

    def create(self, cr, uid, values, context=None):
        if 'standard_price' in values:
            price = values['standard_price']
            if not 10 <= price and values['type'] != 'service':
                raise osv.except_osv(
                    ('No Precio'),
                    ('El precio de costo tiene que ser mayor a 10')
                )
        return super(product_template, self).create(cr, uid, values, context=context)

    def write(self, cr, uid, ids, values, context=None):
        if 'standard_price' in values:
            price = values['standard_price']
            if not 10 <= price:
                raise osv.except_osv(
                    ('No Precio'),
                    ('El precio de costo tiene que ser mayor a 10')
                )
        return super(product_template, self).write(cr, uid, ids, values, context=context)


product_template()


class product_product(osv.osv):
    _inherit = 'product.product'

    def validate_name(self, cr, uid, name, context=None):
        if len(name) > 3:
            if name.isdigit():
                raise osv.except_osv(
                    _('No Numeros'),
                    _('El campo debe tener almenos alguna letra')
                )
        else:
            raise osv.except_osv(
                _('No Longitud Permitida'),
                _('El campo debe almenos 4 carácteres')
            )

        return True

    def create(self, cr, uid, values, context=None):
        if 'name' in values:
            name = values['name']
            self.validate_name(cr, uid, name)
        return super(product_product, self).create(cr, uid, values, context=context)

    def write(self, cr, uid, ids, values, context=None):
        if 'name' in values:
            name = values['name']
            self.validate_name(cr, uid, name)
        return super(product_product, self).write(cr, uid, ids, values, context=context)


product_product()
