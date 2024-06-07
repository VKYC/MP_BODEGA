from odoo import api, fields, models
from datetime import timedelta, datetime


class StockRequestOrder(models.Model):
    _inherit = "stock.request.order"

    def btn_use_template(self):
        view_id = self.env.ref('stock_request_template.template_order_wizard_tree')
        return {
            'name': 'Selecciona tu plantilla',
            'view_mode': 'tree',
            'res_model': 'stock.order.template.wizard',
            # 'domain': [('order_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'target': 'new',
            'view_id': view_id.id,
        }
