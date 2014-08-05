# coding= utf-8

import time

from osv import fields, osv
from tools.translate import _
import openerp.addons.decimal_precision as dp


class fleet_vehicle(osv.Model):
    _inherit = 'fleet.vehicle'
    _description = "Gestion de Vehiculos"

    def _check_unique(self, cr, uid, ids, context=None):
        vehicle_id = self.search(cr, uid, [])
        lst = [
            obj_vehicle.license_plate.lower()
            for obj_vehicle in self.browse(cr, uid, vehicle_id, context=context)
            if obj_vehicle.license_plate and obj_vehicle.id not in ids
        ]
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.license_plate and \
               self_obj.license_plate.lower() in lst:
                return False
            return True

    _columns = {
        'license_plate':  fields.char('License Plate', size=7, required=True, help='License plate number of the vehicle (ie: plate number for a car)'),
        'res_partner_id': fields.many2one('res.partner', 'Cliente', ),
        'nro_chasis': fields.char('Nro Chasis', size=32),
        'motor': fields.char('Motor', size=32),
    }

    _constraints = [(_check_unique, 'El numero de placa ya existe', ['license_plate'])]


fleet_vehicle()


class surmotors_fleet_vehicle_log_contract(osv.osv):
    _inherit = "fleet.vehicle.log.contract"
    _description = "Detalles del contrato"

    def contract_close(self, cr, uid, ids, context=None):
        mrp_production = self.pool.get('mrp.production')
        obj_fleet_contract = self.browse(cr, uid, ids, context=context)

        for fleet_contract in obj_fleet_contract:
            for product in fleet_contract.contact_service_ids:
                new_op = mrp_production.product_id_change(cr, uid, ids, product.product_id.id)
                new_op['value']['product_id'] = product.product_id.id
                new_op['value']['contract'] = fleet_contract.id
                new_op['value']['ubication'] = fleet_contract.center_production.id
                mrp_production.create(cr, uid, new_op['value'], context=context)

        return self.write(cr, uid, ids, {'state': 'closed'}, context=context)

    def _search_routing(self, cr, uid, mrp_bom_id):
        if not mrp_bom_id:
            return False
        mrp_bom = self.pool.get('mrp.bom')
        mrp_bom_id = mrp_bom.browse(cr, uid, mrp_bom_id)
        return mrp_bom_id.routing_id.id

    def create_service(self, cr, uid, ids, context=None):
        mrp_production = self.pool.get('mrp.production')
        mrp_bom = self.pool.get('mrp.bom')
        fleet_vehicle_service = self.pool.get('fleet.vehicle.log.contract.service')
        for self_obj in self.browse(cr, uid, ids, context=context):
            for obj_detail_service in self_obj.contact_service_ids:
                if obj_detail_service.state == 'generate':
                    args = [
                        ('product_id', '=', obj_detail_service.product_id.id),
                        ('sequence', '=', 0)
                    ]
                    mrp_bom_id = mrp_bom.search(cr, uid, args)
                    bom_id = mrp_bom_id[0] if mrp_bom_id else False
                    routing_id = self._search_routing(cr, uid, bom_id)
                    values = {
                        'contract': self_obj.id,
                        'product_id': obj_detail_service.product_id.id,
                        'product_uom': 1,
                        'bom_id': bom_id,
                        'routing_id': routing_id
                    }
                    mrp_production.create(cr, uid, values, context=context)
                    fleet_vehicle_service.write(cr, uid, obj_detail_service.id, {'state': 'generated'})

        return True
        #return self.write(cr, uid, ids, {'state': 'closed'}, context=context)

    def on_change_vehicle(self, cr, uid, ids, vehicle_id, context=None):
        if not vehicle_id:
            return {}

        pool_vehicle = self.pool.get('fleet.vehicle')
        dicc = super(surmotors_fleet_vehicle_log_contract, self).on_change_vehicle(cr, uid, ids, vehicle_id, context)
        partner_id = pool_vehicle.browse(cr, uid, vehicle_id, context=context).res_partner_id.id
        dicc['value']['res_partner_id'] = partner_id
        return dicc

    def get_total(self, cr, uid, ids, fields, arg, context):
        dic = {}
        for price in self.browse(cr, uid, ids, context=context):
            dic[price.id] = {'total': 0.0}
            val = 0.0
            for items in price.contact_service_ids:
                val += items.price_unit
            dic[price.id] = val
        return dic

    def open(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current vehicle """
        if context is None:
            context = {}
        if context.get('xml_id'):
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid, 'surmotors', context['xml_id'], context=context)
            res['context'] = context
            for x in self.browse(cr, uid, ids):
                vehiculo_id = x.vehicle_id.id
                res['context'].update({'default_vehicle_id': vehiculo_id})
            return res
        return False

    def contract_reserve(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'reserve'}, context=context)

    _columns = {
        'res_partner_id': fields.many2one('res.partner', 'Cliente', required=True),
        'contact_service_ids': fields.one2many('fleet.vehicle.log.contract.service', 'contact_id', 'Servicios',),
        'total': fields.function(get_total, digits_compute=dp.get_precision('Account'), string='Total'),
        'state': fields.selection([('open', 'In Progress'), ('reserve', 'Reservado'), ('cancel','Cancelar'), ('closed', 'Ingresado'),], 'Status', readonly=True, help='Choose wheter the contract is still valid or not'),
        'date_reserve': fields.date("Fecha de Reserva"),
        'center_production': fields.many2one('mrp.workcenter', 'Centro de Produccion', domain="[('ubication', '=', 'b')]",required=True),
        'tire': fields.boolean('Llantas de Repuesto'),
        'hydraulic_jack': fields.boolean('Gata Hidraulica'),
        'odometer': fields.float('Valor de Odómetro'),
        'odometer_unit': fields.selection([('kilometers', 'kilometros')]),
        'notes': fields.text('Notas'),
        'attachment_rel': fields.many2many('ir.attachment', 'fleet_vehicle_log_contract_attachment', 'fleet_vehicle_log_contract', 'attachment_id', 'Attachments'),
    }

    _defaults = {
        'date_reserve': lambda *a: time.strftime('%Y-%m-%d'),
        'odometer_unit': 'kilometers'
    }

    def create(self, cr, uid, values, context=None):
        print "create \n values: %s" % values
        contract_super = super(surmotors_fleet_vehicle_log_contract, self).create(cr, uid, values, context=context)
        service_ids = values['contact_service_ids']

        if len(service_ids) == 0:
            raise osv.except_osv(_('Error'), _('La Pestaña Servicios no puede estar vacia'))

        pool_vehicle_cost = self.pool.get('fleet.vehicle.cost')
        pool_mrp_bom = self.pool.get('mrp.bom')
        pool_mrp_routing = self.pool.get('mrp.routing')
        pool_mrp_routing_workcenter = self.pool.get('mrp.routing.workcenter')

        produc_val = values['contact_service_ids']
        for obj_product in produc_val:
            product_id = obj_product[2]['product_id']
            mrp_bom_id = pool_mrp_bom.search(cr, uid, [('product_id', '=', product_id)])
            mrp_bom_id = pool_mrp_bom.search(cr, uid, [('product_id', '=', product_id)])
            mrp_bom = pool_mrp_bom.browse(cr, uid, mrp_bom_id)
            contract = self.browse(cr, uid, contract_super)
            for obj_mrp_bom in mrp_bom:
                routing = pool_mrp_routing.browse(cr, uid, obj_mrp_bom.routing_id.id)
                mrp_routing_workcenter_id = pool_mrp_routing_workcenter.search(cr, uid, [('routing_id', '=', routing.id)])
                mrp_routing_workcenter = pool_mrp_routing_workcenter.browse(cr, uid, mrp_routing_workcenter_id)
                total = 0.0
                for obj_mrp_routing_workcenter in mrp_routing_workcenter:
                    total += obj_mrp_routing_workcenter.hour_nbr
                    print total
                pool_vehicle_cost.create(cr, uid, {'horas_plan': total, 'contract_id': contract.id})

        service_ids = values['contact_service_ids']

        return contract_super


surmotors_fleet_vehicle_log_contract()


class fleet_vehicle_log_contract_service(osv.osv):
    _name = "fleet.vehicle.log.contract.service"
    _description = "Servicios"

    def on_change_product(self, cr, uid, ids, product_id, context=None):
        dic = {'value': {}}
        obj_product = self.pool.get('product.product').browse(cr, uid, product_id)
        dic['value']['price_unit'] = obj_product.list_price
        return dic

    def _get_state(self, cr, uid, context=None):
        return (
            ('generate', 'Por generar'),
            ('generated', 'Generado')
        )

    _columns = {
        'product_id': fields.many2one('product.product', 'Servicio'),
        'price_unit': fields.float('Precio'),
        'contact_id': fields.many2one('fleet.vehicle.log.contract', 'contact'),
        'odometer_unit': fields.selection((
            ('kilometers', 'kilometros'),
            ('miles', 'Millas')), 'kilometraje'),
        'state': fields.selection(_get_state, 'Estado')
    }

    _defaults = {
        'state': 'generate'
    }


fleet_vehicle_log_contract_service()


class surmotors_fleet_vehicle_log_fuel(osv.osv):
    _inherit = "fleet.vehicle.log.fuel"
    _description = "Detalles del estado inicial"

    _columns = {
        'llantas': fields.boolean('Llantas de Repuesto'),
        'gata': fields.boolean('Gata Hidraulica'),
        'fallos': fields.boolean('Desperfectos'),
        'odometer_unit': fields.selection((
            ('kilometers', 'kilometros'),
            ('miles', 'Millas')), 'kilometraje'),
        'attachment_rel': fields.many2many('ir.attachment', 'fleet_vehicle_log_fuelr_attachment', 'fleet_vehicle_log_fuel_id', 'attachment_id', 'Attachments'),
    }

    _defaults = {
        'llantas': lambda *a: 0,
        'gata': lambda *a: 0,
        'fallos': lambda *a: 0,
    }


surmotors_fleet_vehicle_log_fuel()
