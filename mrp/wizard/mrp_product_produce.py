# coding= utf-8


from openerp.osv import osv

class mrp_product_produce(osv.osv_memory):
    _inherit = 'mrp.product.produce'

    def do_produce(self, cr, uid, ids, context=None):
        return super(mrp_product_produce, self).do_produce(cr, uid, ids, context)
