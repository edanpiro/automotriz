# coding= utf-8

import time

from report import report_sxw


class report_stock(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(report_stock, self).__init__(cr, uid, name, context=context)
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
        # context = self.context

        result = []
        product = self.pool.get('product.product')
        product_ids = product.search(cr, uid, [('type', '=', 'product')])

        for obj_product in product.browse(cr, uid, product_ids):
            result.append({
                'name': obj_product.name,
                'qty_available': obj_product.qty_available
            })

        print "result", result
        return result


report_sxw.report_sxw('report.ReportStock', 'stock.inventory', 'addons/automotriz/stock/report/stock_product.rml', parser=report_stock, header=False)
