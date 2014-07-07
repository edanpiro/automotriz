# encoding: utf-8

from osv import osv, fields
from openerp import netsvc
from tools.translate import _

import time


class production(osv.osv):
    _name = 'mrp.production'

    _inherit = 'mrp.production'

    def action_confirm(self, cr, uid, ids, context=None):
        # original
        """ Confirms production order.
        @return: Newly generated Shipment Id.
        """
        shipment_id = False
        wf_service = netsvc.LocalService("workflow")
        uncompute_ids = filter(lambda x:x, [not x.product_lines and x.id or False for x in self.browse(cr, uid, ids, context=context)])
        self.action_compute(cr, uid, uncompute_ids, context=context)
        for production in self.browse(cr, uid, ids, context=context):
            shipment_id = self._make_production_internal_shipment(cr, uid, production, context=context)
            produce_move_id = self._make_production_produce_line(cr, uid, production, context=context)
            # Take routing location as a Source Location.
            source_location_id = production.location_src_id.id
            if production.bom_id.routing_id and production.bom_id.routing_id.location_id:
                source_location_id = production.bom_id.routing_id.location_id.id

            for line in production.product_lines:
                consume_move_id = self._make_production_consume_line(cr, uid, line, produce_move_id, source_location_id=source_location_id, context=context)
                shipment_move_id = self._make_production_internal_shipment_line(cr, uid, line, shipment_id, consume_move_id,\
                                 destination_location_id=source_location_id, context=context)
                self._make_production_line_procurement(cr, uid, line, shipment_move_id, context=context)
            wf_service.trg_validate(uid, 'stock.picking', shipment_id, 'button_confirm', cr)
            production.write({'state':'confirmed'}, context=context)
        # fin original
            bahia = self.pool.get('mrp.workcenter').state_busy(cr, uid, production.contract.center_production.id, context)
            if bahia:
                pass
            else:
                raise osv.except_osv(_('Error'),_("La bahia se encuentra ocupada favor de liberarla o escoger otra bahia en el contrato"))
            #obj_workcenter_line = self.pool.get('mrp.production.workcenter.line')
            #search = obj_workcenter_line.search(cr, uid, [('production_id', 'in', ids)])
            #print "search",len(search)

        return shipment_id

    def action_production_end(self, cr, uid, ids, context=None):
        # original
        """ Changes production state to Finish and writes finished date.
        @return: True
        """
        for production in self.browse(cr, uid, ids):
            self._costs_generate(cr, uid, production)
        write_res = self.write(cr, uid, ids, {'state': 'done', 'date_finished': time.strftime('%Y-%m-%d %H:%M:%S')})
        # fin original
        self.pool.get('mrp.workcenter').state_free(cr, uid, production.contract.center_production.id, context)
        return write_res

    def _get_progress(self, cr, uid, ids, field, arg, context=None):
        result = {}
        obj_production = self.browse(cr, uid, ids, context=context)

        for production in obj_production:
            obj_workcenter_line = self.pool.get('mrp.production.workcenter.line')
            quantity = obj_workcenter_line.search(cr, uid, [('production_id', '=', production.id)])
            total = obj_workcenter_line.search(cr, uid, [('production_id', '=', production.id), ('state', '=', 'done')])
            try:
                percentage = (100.0 * len(total))/len(quantity)
                result[production.id] = percentage
            except:
                result[production.id] = 0.00
        return result

    def onchange_ubication(self, cr, uid, ids, contract_id):
        value = {}
        pool_contract = self.pool.get('fleet.vehicle.log.contract')

        center_production = pool_contract.browse(cr, uid, contract_id)
        value['ubication'] = center_production.center_production.id

        return {'value': value}

    _columns = {
        'contract': fields.many2one('fleet.vehicle.log.contract', 'Ref. Contrato', required=True),
        'barra': fields.function(_get_progress, method=True, string='progreso', type='float'),
        'ubication': fields.many2one('mrp.workcenter', 'Centro de Produccion',domain="[('ubication', '=', 'b')]"),
    }


production()


class mrp_workcenter_line(osv.osv):

    _inherit = 'mrp.production.workcenter.line'

    def modify_production_order_state(self, cr, uid, ids, action):
        """ Modifies production order state if work order state is changed.
        @param action: Action to perform.
        @return: Nothing
        """
        work_center_pool = self.pool.get('mrp.workcenter')
        wf_service = netsvc.LocalService("workflow")
        prod_obj_pool = self.pool.get('mrp.production')
        oper_obj = self.browse(cr, uid, ids)[0]
        prod_obj = oper_obj.production_id
        if action == 'start':
               if prod_obj.state =='confirmed':
                   prod_obj_pool.force_production(cr, uid, [prod_obj.id])
                   wf_service.trg_validate(uid, 'mrp.production', prod_obj.id, 'button_produce', cr)
               elif prod_obj.state =='ready':
                   wf_service.trg_validate(uid, 'mrp.production', prod_obj.id, 'button_produce', cr)
               elif prod_obj.state =='in_production':
                   work_center_pool.state_busy(cr, uid, oper_obj.workcenter_id.id)
                   return
               else:
                   raise osv.except_osv(_('Error!'),_('Manufacturing order cannot be started in state "%s"!') % (prod_obj.state,))
               work_center_pool.state_busy(cr, uid, oper_obj.workcenter_id.id)
        else:
            oper_ids = self.search(cr,uid,[('production_id','=',prod_obj.id)])
            obj = self.browse(cr,uid,oper_ids)
            flag = True
            for line in obj:
                if line.state != 'done':
                     flag = False
            if flag:
                for production in prod_obj_pool.browse(cr, uid, [prod_obj.id], context= None):
                    if production.move_lines or production.move_created_ids:
                        prod_obj_pool.action_produce(cr,uid, production.id, production.product_qty, 'consume_produce', context = None)
                wf_service.trg_validate(uid, 'mrp.production', oper_obj.production_id.id, 'button_produce_done', cr)
            work_center_pool.state_free(cr, uid, oper_obj.workcenter_id.id)
        return


mrp_workcenter_line()


class mrp_bom(osv.osv):
    _inherit = 'mrp.bom'


mrp_bom()
