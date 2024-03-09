from odoo import api, fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.onchange('product_uom_qty')
    def onchange_product_uom_qty(self):
        for move_id in self:
            if move_id.product_id and move_id.product_uom_qty == 0:
                raise UserError(f"No puede ser la cantidad de la demanda 0 para el producto: "
                                f"{move_id.product_id.display_name}")
