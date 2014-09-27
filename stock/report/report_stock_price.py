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

        sql = """
        SELECT distinct(product_id), sum(product_qty) as product_qty, sum(value) as value
        FROM report_stock_inventory
        WHERE state='done' and location_type='internal'
        GROUP BY product_id
        """

        cr.execute(sql)
        recordset = self.cr.dictfetchall()
        result = []

        if recordset:
            for row in recordset:
                product_name = product.read(cr, uid, row['product_id'], ['name_template'])
                result.append({
                    'product_id': product_name['name_template'],
                    'product_qty': int(row['product_qty']),
                    'value': "{:.2f}".format(row['value']),
                })

        return result


report_sxw.report_sxw('report.ReportPrice', 'stock.move', 'addons/automotriz/stock/report/stock_price.rml', parser=report_reception, header=True)
