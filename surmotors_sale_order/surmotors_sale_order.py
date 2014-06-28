<<<<<<< HEAD
# coding= utf-8


from osv import fields, osv


=======
# -*- coding: utf-8 -*-
from osv import fields, osv

>>>>>>> f8a9589ef4ac1ea8f890d7a038caadf3d943f095
class surmotors_sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"
    _description = "Sale Order"

    def on_change_contact(self, cr, uid, ids, contact_id, context=None):
<<<<<<< HEAD
        # values = {}
=======
        values={}
>>>>>>> f8a9589ef4ac1ea8f890d7a038caadf3d943f095
        if not contact_id:
            return {}
        obj_fleet_vehicle_log_contract = self.pool.get("fleet.vehicle.log.contract").browse(cr, uid, contact_id, context=context)

<<<<<<< HEAD
        # product = {}
        lista_detalles = []

        for items in obj_fleet_vehicle_log_contract.contact_service_ids:
            lista_detalles.append({
                'product_id': items.product_id.id,
                'name': items.product_id.name,
                'product_uom_qty': 1,
                'price_unit': items.product_id.list_price,
                'delay': 0,
                'type': 'make_to_stock',
                'product_uom': items.product_id.uom_id.id,
                'state': 'draft'
            })

        values = {
            'value': {
                'partner_id': obj_fleet_vehicle_log_contract.res_partner_id.id,
                'order_line': lista_detalles
            }
        }
        # values["value"] = {"partner_id": obj_fleet_vehicle_log_contract.res_partner_id.id, 'order_line': lista_detalles, }
        return values

    _columns = {
        # 'type_service': fields.many2one('fleet.service.type', 'Tipo de Servicio', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},),
        'contact': fields.many2one('fleet.vehicle.log.contract', 'Ref Contrato', required=True)
    }


surmotors_sale_order()
=======
        product = {}
        lista_detalles = []

        for items in obj_fleet_vehicle_log_contract.contact_service_ids:
            lista_detalles.append({'product_id': items.product_id.id,
            	                   'name': items.product_id.name,
            	                   'product_uom_qty': 1,
            	                   'price_unit': items.product_id.list_price,
            	                   'delay': 0,
            	                   'type': 'make_to_stock',
            	                   'product_uom': items.product_id.uom_id.id,
            	                   'state': 'draft',
            	                   })

        values["value"] = {"partner_id": obj_fleet_vehicle_log_contract.res_partner_id.id, 'order_line': lista_detalles, }
        return values

    _columns = {
        'type_service' : fields.many2one('fleet.service.type', 'Tipo de Servicio', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},),
        'contact': fields.many2one('fleet.vehicle.log.contract', 'Ref. Contrato')
    }

surmotors_sale_order()

>>>>>>> f8a9589ef4ac1ea8f890d7a038caadf3d943f095
