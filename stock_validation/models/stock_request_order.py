from odoo import api, fields, models


class StockRequestOrder(models.Model):
    _inherit = "stock.request.order"

    @api.model
    def create(self, vals):
        order_id = super(StockRequestOrder, self).create(vals)
        activity_type_id = self.env['mail.activity.type'].search([('id', '=', 4)])
        order_id.activity_schedule(
            activity_type_id=activity_type_id.id,
            summary='test_summary',
            note='Note',
            user_id=order_id.create_uid.id,
            date_deadline=order_id.expected_date
        )
        return order_id
