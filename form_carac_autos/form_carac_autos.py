# -*- coding: utf-8 -*-

from osv import osv, fields

class caract_surmotors_fleet_vehicle_log_contract(osv.osv):
    _name = "fleet.vehicle.log.contract"
    _inherit = "fleet.vehicle.log.contract"
    _description = 'Formulario Caracteristicas Autos'

    _columns = {
        'name_car': fields.char('Nombre', help = "Ingresa Nombre del Auto"),
        'descrip_car': fields.text('Descripcion', help = "Ingresa una descripcion")
    }

caract_surmotors_fleet_vehicle_log_contract()