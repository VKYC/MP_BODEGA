from odoo import models, fields
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    qty_on_hand = fields.Float(compute='compute_qty_on_hand', string='Cantidad disponible')

    def compute_qty_on_hand(self):
        for picking_id in self:
            if picking_id and picking_id.location_id and picking_id.product_id:
                available_qty = self.env["stock.quant"].\
                    _get_available_quantity(picking_id.product_id, picking_id.location_id)
                if picking_id.product_id and picking_id.location_id:
                    if available_qty <= 0:
                        raise UserError(f"No hay cantidad disponible de productos: "
                                        f"{picking_id.product_id.display_name}")
                    elif available_qty == picking_id.qty_done or available_qty <= picking_id.qty_done:
                        picking_id.qty_done = available_qty
                        picking_id.qty_on_hand = available_qty
                    else:
                        picking_id.qty_on_hand = available_qty
                else:
                    picking_id.qty_on_hand = 0
            else:
                picking_id.qty_on_hand = 0
