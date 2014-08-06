# coding= utf-8


from osv import osv


class hr_employee(osv.osv):
    _inherit = 'hr.employee'

    def create(self, cr, uid, values, context=None):
        partner = self.pool.get('res.partner')

        if 'name' in values:
            name = values['name']
            if name:
                partner.validate_name(cr, uid, name)

        if 'work_email' in values:
            work_email = values['work_email']
            if work_email:
                partner.validate_email(cr, uid, work_email)
        return super(hr_employee, self).create(cr, uid, values, context=context)

    def write(self, cr, uid, ids, values, context=None):
        partner = self.pool.get('res.partner')

        if 'name' in values:
            name = values['name']
            partner.validate_name(cr, uid, name)

        if 'work_email' in values:
            work_email = values['work_email']
            partner.validate_email(cr, uid, work_email)
        return super(hr_employee, self).write(cr, uid, ids, values, context=context)


hr_employee()
