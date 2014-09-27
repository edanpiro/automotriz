# coding = utf-8


from osv import osv


class stock_report(osv.osv_memory):
    _name = 'stock.report'

    def stock_report(self, cr, uid, ids, context=None):
        datas = {
            'ids': context.get('active_ids', [])
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'ReportStock',
            'datas': datas
        }


stock_report()


class stock_reception(osv.osv_memory):
    _name = 'stock.reception'

    def stock_reception(self, cr, uid, ids, context=None):
        datas = {
            'ids': context.get('active_ids', [])
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'ReportReception',
            'datas': datas
        }


stock_reception()


class stock_price(osv.osv_memory):
    _name = 'stock.price'

    def stock_price(self, cr, uid, ids, context=None):
        datas = {
            'ids': context.get('active_ids', [])
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'ReportPrice',
            'datas': datas
        }
