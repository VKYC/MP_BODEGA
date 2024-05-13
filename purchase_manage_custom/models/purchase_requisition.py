from odoo import fields, models, api
from odoo.exceptions import UserError


class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'

    account_date = fields.Date(string='Fecha de cotabilizacion')
    amount_account_auth = fields.Date(string='Fecha de cotabilizacion')
    amount_account = fields.Date(string='Fecha de cotabilizacion')
    company_currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency of the Payment Transaction",
        required=True,
        default=lambda self: self.env.user.company_id.currency_id,
    )
    move_id = fields.Many2one(
        comodel_name="stock.move",
        string="Move",
    )
    qty_to_approve = fields.Float(string='Cantidad a aprobar', default=0)
    document_approve = fields.Selection(selection=[
        ("solicitud_presupuesto", "Solicitudes de Presupuesto"),
        ("orden_compra", "Orden de Compra")
    ], string='Documento a Aprobar')
    employee_bank_line_ids = fields.One2many(
        comodel_name='employee.bank.line',
        inverse_name='employee_id', string='Cuentas Bancarias'
    )



class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    @api.model_create_multi
    def create(self, vals_list):
        records = super(PurchaseRequisition, self).create(vals_list)
        if self.user_has_groups("purchase_manage_custom.group_purchase_user_purchase"):
            raise UserError("No crear registros.")
        return records

    def write(self, vals):
        if self.user_has_groups("purchase_manage_custom.group_purchase_user_purchase"):
            raise UserError("No puede editar.")
        res = super(PurchaseRequisition, self).write(vals)
        return res
