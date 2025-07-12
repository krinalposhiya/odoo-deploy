

from odoo import models, fields, api

class CustomProductCategory(models.Model):
    _name = 'custom.product.category'
    _description = 'Product Category'

    name = fields.Char(string="Category Name", required=True)
    code = fields.Char(string="Code")
