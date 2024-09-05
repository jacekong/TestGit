from odoo import fields, models

class ProductCategory(models.Model):
    _inherit = 'product.category'
    
    odoo_app = fields.Boolean(string='Odoo App', default=False)
    
class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    module_id = fields.Many2one(
        'project.module',
        string='Module',
        )
    link = fields.Char(string='Link')
    support_ce = fields.Boolean(string='Support CE')
    support_ee = fields.Boolean(string='Support EE')
    install_seq = fields.Integer(string='Installing Sequence')
    odoo_app = fields.Boolean('product.category',related='categ_id.odoo_app')
    app_available = fields.Boolean(string='App Available')
    