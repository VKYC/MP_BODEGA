from odoo import models, fields, api
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    qty_on_hand = fields.Float(compute='compute_qty_on_hand', string='Cantidad disponible')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Etiquetas Analiticas',
                                        store=True, readonly=False, check_company=True, copy=True)

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if 'qty_done' in vals:
                qty_done = val['qty_done']
                product_id = self.env['product.product'].search([('id', '=', val['product_id'])])
                location_id = self.env['stock.location'].search([('id', '=', val['location_id'])])
                if qty_done != 0 and product_id and location_id:
                    available_qty = self.env["stock.quant"].\
                        _get_available_quantity(product_id, location_id)
                    if self._context.get('active_model') == 'stock.picking.type':
                        if available_qty <= 0:
                            val['qty_done'] = 0
                        elif available_qty == qty_done or available_qty <= qty_done:
                            val['qty_done'] = available_qty
        return super(StockMoveLine, self).create(vals)

    @api.onchange('product_id', 'location_id')
    def compute_qty_on_hand(self):
        for picking_id in self:
            if picking_id and picking_id.product_id and picking_id.location_id:
                available_qty = self.env["stock.quant"].\
                    _get_available_quantity(picking_id.product_id, picking_id.location_id)
                if picking_id.state == 'done':
                    picking_id.qty_on_hand = available_qty
                else:
                    if picking_id:
                        if picking_id.product_id and picking_id.location_id:
                            if available_qty <= 0:
                                picking_id.qty_on_hand = 0
                            elif available_qty == picking_id.qty_done or available_qty <= picking_id.qty_done:
                                picking_id.qty_done = available_qty
                                picking_id.qty_on_hand = available_qty
                            else:
                                picking_id.qty_on_hand = available_qty
                        else:
                            picking_id.qty_on_hand = 0
                    else:
                        picking_id.qty_on_hand = 0
            else:
                picking_id.qty_on_hand = 0
