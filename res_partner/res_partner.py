# coding= utf-8

import re

from tools.translate import _


from osv import fields, osv


class res_partner(osv.osv):
    _inherit = "res.partner"
    _description = "Clientes"

    _columns = {
        'res_partner_ids': fields.one2many('fleet.vehicle', 'res_partner_id', 'Vehiculos'),
        'dni': fields.char('DNI', size=8),
        'vat': fields.char('TIN', size=11, help="Tax Identification Number. Check the box if this contact is subjected to taxes. Used by the some of the legal statements."),
        'phone': fields.char('Phone', size=7),
        'mobile': fields.char('Mobile', size=9),
        'country_id': fields.many2one('res.country', 'Country'),
    }

    _defaults = {
        'country_id': 175
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

        if 'phone' in values:
            phone = values['phone']

        return super(res_partner, self).create(cr, uid, values, context=context)

    def check_ruc(self, cr, uid, ids, context=None):
        partner_id = self.search(cr, uid, [])
        lst = [
            self_obj.vat
            for self_obj in self.browse(cr, uid, partner_id, context=context)
            if self_obj.name and self_obj.id not in ids
        ]

        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.name is lst:
                return False
            return True

    def write(self, cr, uid, ids, values, context=None):
        if 'name' in values:
            name = values['name']
            self.validate_name(cr, uid, name)
        return super()

res_partner()
