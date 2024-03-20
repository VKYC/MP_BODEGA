from odoo import api, fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    qty_on_hand = fields.Float(compute='compute_qty_on_hand', string='Cantidad disponible')

    @api.onchange('product_id', 'location_id')
    def compute_qty_on_hand(self):
        for picking_id in self:
            available_qty = self.env["stock.quant"].\
                _get_available_quantity(picking_id.product_id, picking_id.location_id)
            if picking_id.state == 'done':
                picking_id.qty_on_hand = available_qty
            else:
                if picking_id and picking_id.location_id and picking_id.product_id:
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
