# coding= utf-8


from osv import fields, osv


class surmotors_sale_order(osv.osv):
    _name = "sale.order"
    _inherit = "sale.order"
    _description = "Sale Order"

    def on_change_contact(self, cr, uid, ids, contact_id, context=None):
        # values = {}
        if not contact_id:
            return {}
        obj_fleet_vehicle_log_contract = self.pool.get("fleet.vehicle.log.contract").browse(cr, uid, contact_id, context=context)

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

        return values

    _columns = {
        'contact': fields.many2one('fleet.vehicle.log.contract', 'Ref Contrato', required=True)
    }


surmotors_sale_order()
