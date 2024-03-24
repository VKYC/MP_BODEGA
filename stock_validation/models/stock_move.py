from odoo import api, fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    qty_on_hand = fields.Float(compute='compute_qty_on_hand', string='Cantidad disponible')

    @api.onchange('product_id', 'location_id')
    def compute_qty_on_hand(self):
        for picking_id in self:
            if picking_id and picking_id.location_id and picking_id.product_id:
                available_qty = self.env["stock.quant"].\
                    _get_available_quantity(picking_id.product_id, picking_id.location_id)
                if picking_id.state == 'done':
                    picking_id.qty_on_hand = available_qty
                else:
                    available_qty = self.env["stock.quant"].\
                        _get_available_quantity(picking_id.product_id, picking_id.location_id)
                    if picking_id.product_id and picking_id.location_id:
                        if available_qty <= 0:
                            picking_id.qty_on_hand = 0
                        elif available_qty == picking_id.quantity_done or available_qty <= picking_id.quantity_done:
                            picking_id.quantity_done = available_qty
                            picking_id.qty_on_hand = available_qty
                        else:
                            picking_id.qty_on_hand = available_qty
                    else:
                        picking_id.qty_on_hand = 0
            else:
                picking_id.qty_on_hand = 0

    @api.onchange('analytic_account_id', 'analytic_tag_ids')
    def onchange_move_ids_without_package(self):
        for move_line_id in (self.picking_id.move_line_nosuggest_ids |
                             self.picking_id.move_line_ids_without_package |
                             self.picking_id.move_line_ids):
            if self.product_id == move_line_id.product_id:
                model_id = (move_line_id.id or move_line_id.id.origin)
                if model_id:
                    line_id = self.env['stock.move.line'].search([('id', '=', model_id)])
                    line_id.sudo().write({
                        "analytic_account_id": self.analytic_account_id.id,
                        "analytic_tag_ids": [(6, 0, self.analytic_tag_ids.ids)]
                    })
