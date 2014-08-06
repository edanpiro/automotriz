# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Edgard Pimentel (<http://edgard86.blogspot.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


import time
from datetime import datetime
import helper

from report import report_sxw


class boleta(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(boleta, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_head': self._get_head,
            'get_details': self._get_details,
        })
        self.cr = cr
        self.uid = uid
        self.context = context

    def _get_head(self, form):
        result = []
        ids = form['values']
        cr = self.cr
        uid = self.uid

        months = {
            '01': 'Enero',
            '02': 'Febrero',
            '03': 'Marzo',
            '04': 'Abril',
            '05': 'Mayo',
            '06': 'Junio',
            '07': 'Julio',
            '08': 'Agosto',
            '09': 'Setiembre',
            '10': 'Octubre',
            '11': 'Noviembre',
            '12': 'Dicembre',
        }

        pool_account_invoice = self.pool.get('account.invoice')
        obj_account_invoice = pool_account_invoice.browse(cr, uid, ids)
        month = obj_account_invoice.date_invoice[5:7]
        day = obj_account_invoice.date_invoice[8:]
        year = obj_account_invoice.date_invoice[3:4]

        date = obj_account_invoice.date_invoice
        date_invoice = datetime.strptime(obj_account_invoice.date_invoice, '%Y-%m-%d')
        date_invoice_convert = datetime.strftime(date_invoice, '%d-%m-%Y')

        if month in months:
            month = months.get(month)

        result.append({
            'date_invoice': date_invoice_convert,
            'customer': obj_account_invoice.partner_id.name,
            'street': obj_account_invoice.partner_id.street,
            'month': month,
            'day': day,
            'year': year,
            'total': "{:.2f}".format(obj_account_invoice.amount_total),
            'total_letters': helper.number_to_letter(str(obj_account_invoice.amount_total)) + "NUEVOS SOLES",
        })

        return result

    def _get_details(self, form):
        result = []
        ids = form['values']
        cr = self.cr
        uid = self.uid

        pool_invoice_line = self.pool.get('account.invoice.line')
        pool_product = self.pool.get('product.product')

        ids_invoice_line = pool_invoice_line.search(cr, uid, [('invoice_id', '=', ids)])
        total = 0
        for obj_invoice_line in pool_invoice_line.browse(cr, uid, ids_invoice_line):
            product = pool_product.read(cr, uid, obj_invoice_line.product_id.id, ['name_template'])
            importe = obj_invoice_line.quantity * obj_invoice_line.price_unit,
            total += importe[0]
            result.append({
                'quantity': obj_invoice_line.quantity,
                'unit': obj_invoice_line.product_id.uom_id.name,
                'description': product['name_template'] if 'name_template' in product else False,
                'price_unit': "{:.2f}".format(obj_invoice_line.price_unit),
                'importe': "{:.2f}".format(importe[0]),
                'total_letters': helper.number_to_letter(str(total)) + "NUEVOS SOLES",
            })


        print "aa", result

        return result


report_sxw.report_sxw('report.boleta', 'account.invoice', 'addons/automotriz/account/report/boleta.rml', parser=boleta, header=False)
