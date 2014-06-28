# -*- coding: utf-8 -*-
from osv import fields, osv

class type_service(osv.osv):
    _name = "type.service"
    _description = "Tipo de servicio"

    _columns = {
        'name' : fields.char('Nombre', size=60, ),
        'description' : fields.text('Descripción'),
    }

type_service()

