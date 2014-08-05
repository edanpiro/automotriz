# coding= utf-8

from osv import osv, fields


class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def _get_type_voucher(self, cr, uid, ids, context=None):
        return (
            ('factura', 'Factura'),
            ('boleta', 'Boleta')
        )

    _columns = {
        'type_voucher': fields.selection(_get_type_voucher, 'Tipo de comprobante'),
        'serie': fields.char('Serie', size=3),
        'number_voucher': fields.char('N° Comprobante')
    }


account_invoice()
