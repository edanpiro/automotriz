# coding= utf-8

import time

from report import report_sxw


class report_reception(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_reception, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'details': self.details
        })
        self.cr = cr
        self.uid = uid
        self.context = context

    def details(self):
        cr = self.cr
        uid = self.uid

        product = self.pool.get('product.product')
        location = self.pool.get('stock.location')

        sql = """
            SELECT
                day, product_id, product_qty, value, type, location_dest_id
            FROM report_stock_move
            WHERE state='done'
        """

        cr.execute(sql)
        recordset = self.cr.dictfetchall()
        result = []

        if recordset:
            for row in recordset:
                product_name = product.read(cr, uid, row['product_id'], ['name_template'])
                location_name = location.read(cr, uid, row['location_dest_id'], ['name'])
                result.append({
                    'day': row['day'],
                    'product_id': product_name['name_template'],
                    'product_qty': int(row['product_qty']),
                    'type': row['type'],
                    'location_dest_id': location_name['name']
                })

        return result


report_sxw.report_sxw('report.ReportReception', 'stock.move', 'addons/automotriz/stock/report/stock_reception.rml', parser=report_reception, header=True)
