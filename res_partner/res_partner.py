# coding= utf-8

import re

from tools.translate import _


from osv import fields, osv


class res_partner(osv.osv):
    _inherit = "res.partner"
    _description = "Clientes"

    _columns = {
        'res_partner_ids': fields.one2many('fleet.vehicle', 'res_partner_id', 'Vehiculos'),
    }

    def validate_name(self, cr, uid, name, context=None):
        if not (re.search('^[A-Za-z\s]+$', name)):
            raise osv.except_osv(
                _('Alerta'),
                _('El campo nombre solo acepta letras')
            )
        return True

    def create(self, cr, uid, values, context=None):
        if 'name' in values:
            name = values['name']
            self.validate_name(cr, uid, name)

        return super(res_partner, self).create(cr, uid, values, context=context)

    def write(self, cr, uid, ids, values, context=None):
        if 'name' in values:
            name = values['name']
            self.validate_name(cr, uid, name)
        return super()

res_partner()
