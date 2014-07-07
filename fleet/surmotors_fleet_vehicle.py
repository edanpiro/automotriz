# coding= utf-8


from osv import fields, osv


class fleet_vehicle(osv.Model):
    _inherit = "fleet.vehicle"
    _description = "Gestion de Vehiculos"

    def _check_unique(self, cr, uid, ids, context=None):

        for obj_fleet in self.browse(cr, uid, ids):
            cr.execute('select name,license_plate from fleet_vehicle WHERE license_plate=%s', (obj_fleet.license_plate,))
            res_ids = [x[1] for x in cr.fetchone()]
            if len(res_ids) > 0:
                return False
            else:
                return True

    _columns = {
        'license_plate':  fields.char('License Plate', size=7, required=True, help='License plate number of the vehicle (ie: plate number for a car)'),
        'res_partner_id': fields.many2one('res.partner', 'Cliente', ),
        'nro_chasis': fields.char('Nro Chasis', size=32),
        'motor': fields.char('Motor', size=32),
        'equipment_vehicle_id': fields.many2one('equipment.vehicle', 'Tipo de Equipo')
    }

    _constraints = [(_check_unique, 'El numero de placa ya existe', ['license_plate'])]


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
