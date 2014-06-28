# coding= utf-8


from osv import fields, osv


from osv import fields, osv


class surmotors_res_partner(osv.osv):
    _name = "res.partner"
    _inherit = "res.partner"
    _description = "Clientes"

    _columns = {
        'res_partner_ids': fields.one2many('fleet.vehicle', 'res_partner_id', 'Vehiculos', readonly=True),
    }


surmotors_res_partner()
