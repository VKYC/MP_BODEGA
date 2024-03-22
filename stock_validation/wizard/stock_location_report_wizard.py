from odoo import _, api, fields, models
from odoo.exceptions import UserError
from datetime import date, timedelta


class StockLocationReportWizard(models.TransientModel):
    _name = "stock.location.report.wizard"
    _description = "Stock Location Report Wizard"

    init_date_report = fields.Date(string='Fecha de inicio', required=True)
    end_date_report = fields.Date(string='Fecha de fin', required=True)

    def confirm_action(self):
        location_ids = self.env['stock.location'].search([
            ('complete_name', 'ilike', 'Holdc/Stock%'),
            ('usage', '=', 'transit')
        ])
        for location_id in location_ids:
            picking_id = self.env['stock.picking'].search([
                ('location_dest_id', '=', location_id.id),
                ('state', '!=', 'cancel'),
                ('create_date', '>=', self.init_date_report),
                ('create_date', '<=', self.end_date_report),
            ], order='create_date desc', limit=1)
            if picking_id:
                location_id.in_date = picking_id.create_date
        self = self.with_context(usage_location_ids=location_ids.ids)
        action = {
            'name': f'Ubicaciones sin movimiento: De la fecha'
                    f' {self.init_date_report.strftime("%d-%m-%Y")} a {self.end_date_report.strftime("%d-%m-%Y")}',
            'view_type': 'tree',
            'view_mode': 'list',
            'view_id': self.env.ref('stock_validation.stock_location_report_tree').id,
            'res_model': 'stock.location',
            'type': 'ir.actions.act_window',
            'domain': [('complete_name', 'ilike', 'Holdc/Stock%'), ('usage', '=', 'transit')],
            'context': {'create': False},
        }

        return action
