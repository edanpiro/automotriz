# coding= utf-8

from osv import osv, fields


class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def _get_type_voucher(self, cr, uid,  context=None):
        return (
            ('factura', 'Factura'),
            ('boleta', 'Boleta')
        )

    _columns = {
        'type_voucher': fields.selection(_get_type_voucher, 'Tipo de comprobante'),
        'serie': fields.char('Serie', size=3),
        'number_voucher': fields.char('N° Comprobante')
    }

    def print_boleta(self, cr, uid, ids, context=None):
        data = {'form': {'values': ids[0]}}
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'boleta',
            'datas': data
        }

    def print_factura(self, cr, uid, ids, context=None):
        data = {'form': {'values': ids[0]}}
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'factura',
            'datas': data
        }


account_invoice()
