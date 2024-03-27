from odoo import api, fields, models
from datetime import timedelta, datetime


class StockRequestOrder(models.Model):
    _inherit = "stock.request.order"

    def _cron_update_terminate_records(self):
        order_ids = self.env['stock.request.order'].search([])
        cancel_automatic = self.env['ir.config_parameter'].sudo().get_param('cancel_stock_request_automatic') or False
        for order_id in order_ids:
            date_end = order_id.expected_date + timedelta(days=5)
            if datetime.now() > date_end and order_id.state != 'done' and cancel_automatic:
                order_id.action_cancel()

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
