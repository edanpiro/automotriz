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
            'report_name': 'RportStock',
            'datas': datas
        }


stock_report()
