# coding= utf-8


from openerp.osv import osv


class mrp_product_produce(osv.osv_memory):
    _inherit = 'mrp.product.produce'

    def do_produce(self, cr, uid, ids, context=None):
        pool_bahia = self.pool.get('mrp.workcenter')
        production_id = context.get('active_id', False)
        if production_id:
            bahia_id = self.pool.get('mrp.production').browse(cr, uid, production_id).ubication
            pool_bahia.state_free(cr, uid, bahia_id.id, context)

        return super(mrp_product_produce, self).do_produce(cr, uid, ids, context)
