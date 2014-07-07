# -*- coding: utf-8 -*-
from osv import osv, fields


class equipment_vehicle(osv.osv):
    _name = "equipment.vehicle"
    _description = "Tipo de Vehiculo"

    _columns = {
        'equipment': fields.char('Tipo de Equipo', size=30),
    }

equipment_vehicle()

