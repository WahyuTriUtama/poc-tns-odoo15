from odoo import models, fields, api


class ProductTemplate(models.Model):
    """inherited product"""
    _inherit = 'product.template'

    branch_id = fields.Many2one("res.branch", string='Branch', store=True,
                                help='Leave this field empty if this product is'
                                     ' shared between all branches'
                                )
    allowed_branch_ids = fields.Many2many('res.branch', store=True,
                                          string="Allowed Branches",
                                          compute='_compute_allowed_branch_ids')

    @api.depends('company_id')
    def _compute_allowed_branch_ids(self):
        for po in self:
            po.allowed_branch_ids = self.env.user.branch_ids.ids
