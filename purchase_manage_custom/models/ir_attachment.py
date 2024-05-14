from odoo import fields, models, api
from odoo.exceptions import UserError


class IrAttachment(models.Model):
    _inherit = "ir.attachment"


    def unlink(self):
        if self.user_has_groups("purchase_manage_custom.group_purchase_user_purchase"):
            raise UserError("No se puede eliminar registros.")
        return super(IrAttachment, self).unlink()
