from odoo import models, fields
from odoo.exceptions import UserError


class Picking(models.Model):
    _inherit = 'stock.picking'

    def write(self, vals):
        if 'move_line_ids_without_package' in vals:
            for val in vals['move_line_ids_without_package']:
                if val[1]:
                    request_int_id = val[1]
                    if not isinstance(request_int_id, int) and 'virtual_' in val[1]:
                        request_int_id = request_int_id.split('_')[1]
                    move_line_id = self.env['stock.move.line'].search([('id', '=', request_int_id)], limit=1)
                    if move_line_id:
                        qty_done = move_line_id.qty_done
                        product_id = move_line_id.product_id
                        location_id = move_line_id.location_id
                        if val[2]:
                            if 'qty_done' in val[2]:
                                qty_done = val[2].get('qty_done')
                            if 'product_id' in val[2]:
                                product_id = self.env['product.product'].search([('id', '=', val[2].get('product_id'))])
                            if 'location_id' in val[2]:
                                location_id = self.env['stock.location'].search([('id', '=', val[2].get('location_id'))])
                            if qty_done != 0 and product_id and location_id:
                                available_qty = self.env["stock.quant"].\
                                    _get_available_quantity(product_id, location_id)
                                if available_qty <= 0:
                                    raise UserError(f"No hay en stock cantidad disponible de productos: "
                                                    f"{product_id.display_name}")
                                elif available_qty == qty_done or available_qty <= qty_done:
                                    val[2]['qty_done'] = available_qty
        return super(Picking, self).write(vals)
