# -*- coding: utf-8 -*-

from osv import fields, osv

class surmotors_fleet_vehicle_cost_tipo(osv.osv):
    _name = "fleet.vehicle.cost.tipo"

    _columns = {
        'name' : fields.char('Nombre', size=100),
    }

surmotors_fleet_vehicle_cost_tipo()

