from odoo import fields, models


class StockLocation(models.Model):
    _inherit = 'stock.location'

    show_in_report = fields.Boolean(compute='_compute_show_report', store=True, compute_sudo=True)
    in_date = fields.Datetime(compute='_compute_in_date', store=True, compute_sudo=True, string='Fecha')

    def _compute_in_date(self):
        for location_id in self:
            picking_id = self.env['stock.picking'].search([
                '|',
                ('location_id', '=', location_id.id),
                ('location_dest_id', '=', location_id.id),
            ], order='create_date desc', limit=1)
            location_id.in_date = picking_id.create_date

    def _compute_show_report(self):
        for location_id in self:
            picking_ids = self.env['stock.picking'].search([
                '|',
                ('location_id', '=', location_id.id),
                ('location_dest_id', '=', location_id.id),
            ])
            if not picking_ids:
                location_id.show_in_report = True
            else:
                location_id.show_in_report = False
