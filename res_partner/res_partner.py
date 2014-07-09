# coding= utf-8


from osv import fields, osv


class res_partner(osv.osv):
    _inherit = "res.partner"
    _description = "Clientes"

    _columns = {
        'res_partner_ids': fields.one2many('fleet.vehicle', 'res_partner_id', 'Vehiculos'),
    }


res_partner()
