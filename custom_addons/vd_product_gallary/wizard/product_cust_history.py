from odoo import models, fields
class ProductHistoryWizard(models.TransientModel):
    _name = 'product.history.wizard'
    _description = 'Wizard to Add Product Sharing History'

    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    product_template_id = fields.Many2one('product.template', string="Product", required=True)
    date_shared = fields.Datetime(string="Date Shared", default=fields.Datetime.now)
    shared_by = fields.Many2one('res.users', string="Shared By", default=lambda self: self.env.user)
    notes = fields.Text(string="Notes")

    def action_add_to_history(self):
        self.ensure_one()
        self.env['product.detail.history'].create({
            'product_template_id': self.product_template_id.id,
            'partner_id': self.partner_id.id,
            'date_shared':self.date_shared,
            'shared_by':self.shared_by.id,
            'notes': self.notes,
        })
        return {'type': 'ir.actions.act_window_close'}
