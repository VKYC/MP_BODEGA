from odoo import api, fields, models


class StockRequestOrder(models.Model):
    _inherit = "stock.request.order"

    @api.model
    def create(self, vals):
        order_id = super(StockRequestOrder, self).create(vals)
        activity_type_id = self.env['mail.activity.type'].search([('id', '=', 4)])
        activity = self.env['mail.activity'].create({
            'activity_type_id': activity_type_id.id,
            'user_id': order_id.create_uid.id,
            'res_id': self.env['ir.model']._get_id('stock.request.order'),
            'res_model_id': self.env['ir.model'].search([('model', '=', 'res.partner')], limit=1).id,
            'summary': 'test_summary',
        })
        return order_id
