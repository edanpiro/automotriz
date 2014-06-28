# -*- coding: utf-8 -*-

from osv import fields, osv

class surmotors_hr_employee(osv.osv):
    _name = "hr.employee"
    _inherit = "hr.employee"

    _columns = {
        'costo_hora' : fields.integer('Costo por hora'),
    }

surmotors_hr_employee()

