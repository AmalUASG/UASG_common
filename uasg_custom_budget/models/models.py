# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class Tag(models.Model):
    
    _name="budget.tags"
    name = fields.Char()
    color = fields.Integer(string='Color Index')

class Department(models.Model):
    _name='department'
    _description="UASG Departments"

    name=fields.Char('Department')
    company = fields.Many2one('res.company')
    department_manager = fields.Many2one('res.users')

class Category(models.Model):
    _name='category'
    _description="Categories"

    name=fields.Char('Category')


class Users(models.Model):

    _inherit = 'res.users'

    uasg_department = fields.Many2one('department')
    uasg_budget_user_type = fields.Selection(string="Budget User Types",selection=[('user','User'),('dept_manager','Department Manager'),('approval','Approval')], default='user')

class Budget(models.Model):
    _name = 'budget'
    _description = 'Budget'
    _inherit = [ 'mail.thread']

    def years_selection(self):

        year_list = []
        for y in range(datetime.now().year, datetime.now().year + 10):
            year_list.append((str(y), str(y)))
        return year_list
    name = fields.Char('Name')
    company_id = fields.Many2one('res.company',name="Company",related='create_uid.company_id', store=True)
    department = fields.Many2one('department',related='create_uid.uasg_department',store=True)
    department_manager = fields.Many2one('res.users',name="Department Manager",related="department.department_manager", store=True)
    year = fields.Selection(selection='years_selection',default="2023")
    duration_from = fields.Date()
    duration_to = fields.Date()
    budget_line = fields.One2many('budget.line','budget_id' , compute='_compute_budget_line')
    state = fields.Selection(selection=[('draft','Draft'),('pending','Pending Approval'),('approved','approved'),], default='draft' ,  tracking=True)
    tag_ids=fields.Many2many('budget.tags', 'budget_tags_rel','budget_id','tag_id', string='Tags', help="Optional tags you may want to assign for custom reporting", ondelete='restrict')
    color = fields.Integer(string='Color Index')
    total_budget_cost = fields.Monetary(compute='_compute_total_budget_cost')
    currency_id = fields.Many2one(string='Company Currency',related='company_id.currency_id', readonly=True)

    def _compute_budget_line (self):
        
        for record in self : 
            line = self.env['budget.line'].search([('budget_id' , '=' , record.id) , ('budget_line_state' , '=' , 'submit')])

            record.budget_line = line

    def _compute_total_budget_cost(self):

        lines = self.env['budget.line'].search([('budget_id', '=', self.id)])
        total_lines_budget = sum(lines.mapped('cost_by_company_currency'))
        self.total_budget_cost = total_lines_budget

    def action_submit(self):

        self.write ({'state' : 'pending'})

    def action_approve(self):

        self.write ({'state' : 'approved'})

    def action_reject(self):

        self.write ({'state' : 'draft'})

class BudgetElements(models.Model):
    _name = 'budget.line'
    _description = 'Budget Elements'
    _inherit = [ 'mail.thread']

    def _get_default_budget_id(self):

        return self.env.context.get('default_budget_id') or self.env.context.get('active_id')
    name = fields.Char('Name' , required="1")
    state = fields.Selection(selection=[('draft','Draft'),('pending','Pending Approval'),('approved','approved'),], related='budget_id.state')
    company_id = fields.Many2one('res.company',related='budget_id.company')

    currency_id = fields.Many2one('res.currency',string='Company Currency',default=lambda self: self.env.company.currency_id)
    cost = fields.Monetary()
    cost_by_company_currency = fields.Monetary(compute='_cost_by_company_currency' , store=True)
    description = fields.Text()
    budget_id = fields.Many2one('budget',ondelete='cascade' ,  default=_get_default_budget_id , required=1)
    category_id = fields.Many2one('category')
    company_id = fields.Many2one('res.company',name="Company",related='budget_id.company_id', store=True)
    department = fields.Many2one('department',related='budget_id.department',store=True)
    duration_from = fields.Date()
    duration_to = fields.Date()
    business_company_id = fields.Many2one('res.company',name="Related Company",)
    business_department = fields.Many2one('department', name = "Related Department")
    company_currency_id = fields.Many2one('res.currency' , related='company_id.currency_id',store='True')
    budget_line_state = fields.Selection(selection=[('draft','Draft'),('submit','submitted')], default='draft' ,  tracking=True)

    reject_reason = fields.Char()


    def action_submit(self):

        mail_template = self.env['mail.template'].search([('model_id','=','budget.line'),('name','=','Budget demand is submitted')])
        if mail_template : 
            mail_template.send_mail(self.id, force_send=True)

        self.write ({'budget_line_state' : 'submit'})


    @api.depends('cost')
    def _cost_by_company_currency(self):
        if self.currency_id and self.company_id : 
            for record in self : 
                cost_by_company_currency = record.currency_id._convert(
                        abs(record.cost),
                        record.company_id.currency_id,
                        record.company_id,
                        datetime.today())
                record.cost_by_company_currency = cost_by_company_currency
                    


    @api.onchange('business_company_id')
    def get_business_department(self):
        if self.business_company_id is True:
            domain = [('company', '=', self.business_company_id.id)]
        else:
            domain = []
        return {'domain': {'business_department': domain}}




class RejectBudgetLineWizard(models.TransientModel):
    _name = 'reject.budget.line.wizard'
    _description = 'Reject Wizard'


    name = fields.Char('Reasons to Reject')
    budget_line_id = fields.Many2one('budget.line')

    def action_reject(self):

        self.ensure_one()

        mail_template = self.env['mail.template'].search([('model_id','=','budget.line'),('name','=','Budget demand is Rejected')])
        if mail_template : 
            mail_template.send_mail(self.id, force_send=True)


        line = self.env['budget.line'].search([('id','=',self.budget_line_id.id)])

        line.write({'budget_line_state':'draft','reject_reason':self.name})


