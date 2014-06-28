<<<<<<< HEAD
# coding= utf-8


from osv import fields, osv


=======
# -*- coding: utf-8 -*-
from osv import fields, osv

>>>>>>> f8a9589ef4ac1ea8f890d7a038caadf3d943f095
class fleet_vehicle(osv.osv):
    _name = "fleet.vehicle"
    _inherit = "fleet.vehicle"
    _description = "Gestion de Vehiculos"

    _columns = {
        'res_partner_id': fields.many2one('res.partner', 'Cliente', ),
        'nro_chasis': fields.char('Nro Chasis', size=32),
        'motor': fields.char('Motor', size=32),
        'equipment_vehicle_id': fields.many2one('equipment.vehicle', 'Tipo de Equipo')
    }

<<<<<<< HEAD

fleet_vehicle()


class surmotors_fleet_vehicle_cost(osv.osv):
    _name = "fleet.vehicle.cost"
    _inherit = "fleet.vehicle.cost"

    def onchange_empleado(self, cr, uid, ids, empleado_id):
        value = {}
        pool_employee = self.pool.get('hr.employee')

        employee = pool_employee.browse(cr, uid, empleado_id)
        value['costo_hora'] = employee.costo_hora
        value['cargo'] = employee.job_id.id

        return {'value': value}

    def onchange_horas_plan(self, cr, uid, ids, costo_hora, horas_plan):
        return {'value': {'monto_plan': costo_hora * horas_plan}}

    def onchange_horas_reales(self, cr, uid, ids, costo_hora, horas_reales):
        return {'value': {'amount': costo_hora * horas_reales}}

    _columns = {
        'tipo': fields.many2one('fleet.vehicle.cost.tipo', 'Tipo'),
        'empleado': fields.many2one('hr.employee', 'Empleado'),
        'horas_plan': fields.float('Horas Plan.'),
        'ini_plan': fields.date('Ini. Plan.'),
        'fin_plan': fields.date('Fin. plan.'),
        'costo_hora': fields.integer('Costo por hora'),
        'horas_reales': fields.integer('Horas Reales'),
        'fin_real': fields.date('Fin Real'),
        'monto_plan': fields.float('Monto Plan'),
        'cargo': fields.many2one('hr.job', 'Cargo'),
    }


surmotors_fleet_vehicle_cost()
=======
fleet_vehicle()
>>>>>>> f8a9589ef4ac1ea8f890d7a038caadf3d943f095
