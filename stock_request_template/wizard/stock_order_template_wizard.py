from odoo import models, fields


class StockOrderTemplateWizard(models.TransientModel):
    _name = 'stock.order.template.wizard'

    stock_order_id = fields.Many2one(comodel_name='stock.request.order.template',
                                     string='Solicitud', readonly=True)

    def button_add_template(self):
        print('smn')
