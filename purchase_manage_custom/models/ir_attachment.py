from odoo import fields, models, api
from odoo.exceptions import UserError


class IrAttachment(models.Model):
    _inherit = "ir.attachment"


    def unlink(self):
        if self.user_has_groups("purchase_manage_custom.group_purchase_user_purchase"):
            raise UserError("No se puede eliminar registros.")
        return super(IrAttachment, self).unlink()

    @api.model_create_multi
    def create(self, vals_list):
        records = super(IrAttachment, self).create(vals_list)
        if self.user_has_groups("purchase_manage_custom.group_purchase_user_purchase"):
            raise UserError("No crear registros.")
        return records

    def write(self, vals):
        if self.user_has_groups("purchase_manage_custom.group_purchase_user_purchase"):
            raise UserError("No puede editar.")
        res = super(IrAttachment, self).write(vals)
        return res
