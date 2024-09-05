from odoo import api,fields, models

class Project(models.Model):
    _inherit = 'project.project'
    
    ref = fields.Char(string='Reference')
    official_pro_name = fields.Text(string='Ofiicial Project Name')
            
class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    dependency_ids = fields.Many2many(comodel_name='product.product', string='Dependency Module', domain=[('categ_id.odoo_app', '=', True)])
    responsible_by = fields.Many2one('res.users', string='Responsible by')
    deploy_db_dev = fields.Many2one(comodel_name='project.database', string='Deployed Database-Dev')
    deploy_db_pd = fields.Many2one(comodel_name='project.database', string='Deployed Database-Prod')
    deploy_db_std = fields.Many2one(comodel_name='project.database', string='Deployed Database-STD')
    customization_detail_ids = fields.One2many('customization.details', 'task_id', string='Customization Details')
    solution = fields.Html()
    product_id = fields.Many2one('product.product', string='Product', domain=[('categ_id.odoo_app', '=', True)])
    ref_name = fields.Char(related='project_id.ref')
    # new
    is_pain_point = fields.Boolean(string='is Pain Point', default=False)
    is_gap = fields.Boolean(string='is GAP', default=False)
    product_id_required = fields.Boolean(
        compute='_compute_product_id_required', store=True
    )

    @api.depends('stage_id')
    def _compute_product_id_required(self):
        for task in self:
            task.product_id_required = bool(
                task.stage_id and task.stage_id.require_module_name
            )
    
    @api.onchange('task_group_id')
    def onchange_task_group(self):
        # check description
        desc = self.description
        if desc:
            if desc in ['<p><br></p>', '<p>\xa0</p>']:
                self.write({'description': False})
                self.description = self.task_group_id.description
                return
            else:
                return
        self.description = self.task_group_id.description       
    
class FieldType(models.Model):
    _name = 'field.type'
    
    name        = fields.Char(string='Name')
    description = fields.Text(string='Description')
    
class CustomizationDetails(models.Model):
    _name = 'customization.details'
    
    task_id = fields.Many2one(
        'project.task',
        string='Task ID',
        )
    sequence = fields.Integer(string='Sequence')
    description = fields.Text(string='Description')
    link = fields.Char(string='Link')
    tested = fields.Boolean(string='Tested', default=False)
    pass_status = fields.Boolean(string='Pass Status', default=False)
    test_date = fields.Date(string='Test Date')
    tester = fields.Many2one('res.users', string='Tester')
    field_status = fields.Boolean(string='New Field Status', default=False)
    field_name = fields.Char(string='Field Name')
    related_field = fields.Char(string='Related Field')
    field_type = fields.Many2one('field.type', string='Field Type')
    required_field = fields.Boolean(string='Required Field', default=False)
    read_only = fields.Boolean(string='Read Only', default=False)
    stored = fields.Boolean(string='Stored', default=False)    
    pos_in_form_view = fields.Text(string='Position In Form View')
    field_action = fields.Text(string='Field Action')
    field_security_group = fields.Text(string='Field Security Group')
    field_objective = fields.Text(string='Field Objective')
    field_remark = fields.Text(string='Field Remark')
    rec_index = fields.Integer(string='Recno', compute='_compute_index', store=True)
    tester_comment = fields.Text(string='Tester Comment')
    dev_comment = fields.Text(string='Developer Comment')
    # task related fields
    related_menu = fields.Text(related='task_id.related_menu', string='Related Menu')
    customization_id = fields.Many2one(related='task_id.customization_id', string='Customization Type')
    module_id = fields.Many2one(related='task_id.product_id', string='Module & Version')
    dependency_ids = fields.Many2many(related='task_id.dependency_ids', string='Dependency Module')
    deploy_dev = fields.Boolean(related='task_id.deploy_dev', string='To Merge-Dev.')
    deploy_prod = fields.Boolean(related='task_id.deploy_prod', string='To Merge-Master')
    deploy_std = fields.Boolean(related='task_id.deploy_std', string='To Merge-Master STD')
    deploy_status_dev = fields.Boolean(related='task_id.deploy_status_dev', string='Deploy Status-Dev.')
    deploy_db_dev = fields.Many2one(related='task_id.deploy_db_dev', string='Deploy Database-Dev.')
    deploy_description_dev = fields.Text(realted='task_id.deploy_description_dev',string="Deploy Description-Dev")
    deploy_status_prod = fields.Boolean(related='task_id.deploy_status_prod',string='Deploy Status-Prod.')
    deploy_db_pd = fields.Many2one(related='task_id.deploy_db_pd', string='Deploy Database-Prod')
    deploy_description_prod = fields.Text(realted='task_id.deploy_description_prod',string="Deploy Description-Prod")
    deploy_status_std = fields.Boolean(related='task_id.deploy_status_std', string='Deploy Status-STD.')
    deploy_db_std = fields.Many2one(related='task_id.deploy_db_std', string='Deploy Database-STD')
    deploy_description_std = fields.Text(realted='task_id.deploy_description_std',string="Deploy Description-STD")
    
    @api.onchange('tested')
    def oncahnge_test_date(self):
        for rec in self:
            if rec.tested:
                rec.test_date = fields.Date.today()
            else:
                rec.test_date = False
    
    @api.depends('rec_index', 'task_id')
    def _compute_index(self):
        for task in self.mapped('task_id'):
            index = 1
            for lines in task.customization_detail_ids:
                lines.rec_index = index
                index += 1
                
    def action_open_task_form(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Task',
            'view_mode': 'form',
            'res_model': 'project.task',
            'res_id': self.task_id.id,
            'target': 'current',
            'view_id': self.env.ref('project.view_task_form2').id,
        }
                
class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'
    
    require_module_name = fields.Boolean(string="Requiring Module Name", default=False)