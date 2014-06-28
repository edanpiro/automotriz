#encoding: utf-8

from osv import osv, fields

class bahias(osv.osv):
    _name = 'mrp.workcenter'
    _inherit = 'mrp.workcenter'

    def button_ocupar(self, cr, uid, ids, context=None):
        print "entro a ocupar"
        return self.write(cr, uid, ids, {'state': 'busy'}, context=context)

    def state_busy(self, cr, uid, dt, context=None):
        print "context state_busy", context
        center = self.browse(cr, uid, dt)
        if center.state == 'free':
            self.write(cr, uid, dt, {'state': 'busy'}, context=context)
            return True
        else:
            return False

    def state_free(self, cr, uid, ids, context=None):
        #center = self.browse(cr, uid, ids)
        self.write(cr, uid, ids, {'state': 'free'}, context=context)
        return True


    _columns = {
        'state': fields.selection([
            ('free', 'Libre'),
            ('busy', 'Ocupado')], 'Estado'),
        'ubication': fields.selection([
            ('t', 'Taller'),
            ('b', 'Bahia')], 'Tipo de Ubicacion', required=True),
    }

    _defaults = {
        'state': 'free',
    }

bahias()
