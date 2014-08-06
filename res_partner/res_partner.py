# coding= utf-8

import re

from tools.translate import _
from osv import fields, osv


class res_partner(osv.osv):
    _inherit = "res.partner"
    _description = "Clientes"

    def _check_ruc(self, cr, uid, ids, context=None):
        partner_id = self.search(cr, uid, [])
        lst = [
            self_obj.vat
            for self_obj in self.browse(cr, uid, partner_id, context=context)
            if self_obj.vat and self_obj.id not in ids
        ]
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.vat in lst:
                return False
            return True

    def _check_dni(self, cr, uid, ids, context=None):
        partner_id = self.search(cr, uid, [])
        lst = [
            self_obj.dni
            for self_obj in self.browse(cr, uid, partner_id, context=context)
            if self_obj.dni and self_obj.id not in ids
        ]
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.dni in lst:
                return False
            return True

    _columns = {
        'res_partner_ids': fields.one2many('fleet.vehicle', 'res_partner_id', 'Vehiculos'),
        'dni': fields.char('DNI', size=8),
        'vat': fields.char('TIN', size=11, help="Tax Identification Number. Check the box if this contact is subjected to taxes. Used by the some of the legal statements."),
        'phone': fields.char('Phone', size=12),
        'mobile': fields.char('Mobile', size=12),
        'country_id': fields.many2one('res.country', 'Country'),
    }

    _defaults = {
        'country_id': 175
    }

    _constraints = [
        (_check_ruc, 'El numero de RUC ya existe', ['vat']),
        (_check_dni, 'El numero de DNI ya existe', ['dni'])
    ]

    def validate_name(self, cr, uid, name, context=None):
        if not (re.search('^[A-Za-z\s]+$', name)):
            raise osv.except_osv(
                _('Alerta'),
                _('El campo nombre solo acepta letras')
            )
        return True

    def validate_email(self, cr, uid, email, context=None):
        if not (re.search('^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\)]+\.[(a-z)]{2,4}$', email.lower())):
            raise osv.except_osv(
                _('Alerta'),
                _('El correo no es valido')
            )
        return True

    def validate_mobile(self, cr, uid, mobile, context=None):
        if not (re.search('([0]\d{1,2}\-)?\d{9}', mobile)):
            raise osv.except_osv(
                _('Alerta'),
                _('El mobil no es valido')
            )
        return True

    def validate_phone(self, cr, uid, phone, context=None):
        if not (re.search('([0]\d{1,2}-)?\d{3}-\d{4}', phone)):
            raise osv.except_osv(
                _('Alerta'),
                _('El numero de telefono no es valido')
            )
        return True

    def validate_dni(self, cr, uid, dni, context=None):
        if not dni.isdigit():
            raise osv.except_osv(
                _('Alerta'),
                _('El DNI solo debe tener numeros')
            )
        return True

    def validate_vat(self, cr, uid, ruc, context=None):
        if not ruc.isdigit():
            raise osv.except_osv(
                _('Alerta'),
                _('El RUC solo debe tener numeros')
            )
        return True

    def create(self, cr, uid, values, context=None):
        if 'name' in values:
            name = values['name']
            self.validate_name(cr, uid, name)

        if 'phone' in values:
            phone = values['phone']
            if phone:
                self.validate_phone(cr, uid, phone)

        if 'email' in values:
            email = values['email']
            if email:
                self.validate_email(cr, uid, email)

        if 'mobile' in values:
            mobile = values['mobile']
            if mobile:
                self.validate_mobile(cr, uid, mobile)

        if 'dni' in values:
            dni = values['dni']
            if dni:
                self.validate_dni(cr, uid, dni)

        if 'vat' in values:
            vat = values['vat']
            if vat:
                self.validate_vat(cr, uid, vat)

        return super(res_partner, self).create(cr, uid, values, context=context)

    def write(self, cr, uid, ids, values, context=None):
        if 'name' in values:
            name = values['name']
            self.validate_name(cr, uid, name)

        if 'email' in values:
            email = values['email']
            self.validate_email(cr, uid, email)

        if 'phone' in values:
            phone = values['phone']
            self.validate_phone(cr, uid, phone)

        if 'mobile' in values:
            mobile = values['mobile']
            self.validate_mobile(cr, uid, mobile)

        if 'dni' in values:
            mobile = values['dni']
            self.validate_dni(cr, uid, mobile)

        if 'vat' in values:
            vat = values['vat']
            self.validate_vat(cr, uid, vat)

        return super(res_partner, self).write(cr, uid, ids, values, context=context)

res_partner()
