# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError

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
    line_manager = fields.Char(string="Line Manager / Budget Approval Email")


class Category(models.Model):
    _name='category'
    _description="Categories"

    name=fields.Char('Category')




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
    department = fields.Many2one('department')
    department_manager = fields.Many2one('res.users',name="Department Manager",related="department.department_manager", store=True)
    budget_line = fields.One2many('budget.line','budget_id',compute='_compute_budget_line',store=True)Ansha Puthiya Veettil
    state = fields.Selection(selection=[('draft','Draft'),('in_progress','In Progress'),('pending','Pending Approval'),('approved','approved'),], default='draft' ,  tracking=True)
    tag_ids=fields.Many2many('budget.tags', 'budget_tags_rel','budget_id','tag_id', string='Tags', help="Optional tags you may want to assign for custom reporting", ondelete='restrict')
    color = fields.Integer(string='Color Index')
    total_budget_cost = fields.Monetary(compute='_compute_total_budget_cost')
    currency_id = fields.Many2one(string='Company Currency',related='company_id.currency_id', readonly=True)
    budget_type = fields.Selection(selection=[('it_budget','IT Budget'),('other','Other Departments')],default='other')
    approval_line = fields.One2many('approval.line','budget_id')
    reject_reason = fields.Char()
    note = fields.Char(tracking=True)
    department_manager_id = fields.Many2one('uasg.contacts')
    company_id = fields.Many2one('res.company',related='department_manager_id.company_id' , name="Company")

    department_name = fields.Char(related='department_manager_id.department')
    manager = fields.Char(related='department_manager_id.manager_name')
    manager_email = fields.Char(related='department_manager_id.manager_email')

    


    def _compute_budget_line (self):
        
        for record in self : 
            line = self.env['budget.line'].search([('budget_id' , '=' , record.id) ])

            record.budget_line = line


    @api.onchange('company_id')
    def get_department(self):
            
        domain = [('company', '=', self.company_id.id)]

        return {'domain': {'department': domain}}


    @api.onchange('budget_type')
    def department_it(self):

        if self.budget_type == 'it_budget':

            self.department = self.env.user.uasg_department.id

    def _compute_total_budget_cost(self):

        for record in self:

            lines = self.env['budget.line'].search([('budget_id', '=', record.id)])
            total_lines_budget = sum(lines.mapped('cost_by_company_currency'))
            record.total_budget_cost = total_lines_budget

    def action_submit(self):

        if self.budget_type == 'it_budget' :

            mail_template = self.env['mail.template'].sudo().search([('model_id','=','budget'),('name','=','IT Budget Submission')])
            if mail_template : 
                mail_template.send_mail(self.id, force_send=True)

        if self.budget_type == "other":

            mail_template = self.env['mail.template'].sudo().search([('model_id','=','budget'),('name','=','Other Budget Submission')])
            if mail_template : 
                mail_template.send_mail(self.id, force_send=True)


        self.write ({'state' : 'in_progress'})


    def action_submit_2(self):

        if self.budget_type == 'it_budget' :

                self.write ({'state' : 'pending'})

        if self.budget_type == "other":

            mail_template = self.env['mail.template'].sudo().search([('model_id','=','budget'),('name','=','Get Budget Approved')])
            if mail_template : 
                mail_template.send_mail(self.id, force_send=True)

                self.write ({'state' : 'pending'})

        lines = self.budget_line.search([('budget_id','=',self.id)])

        for line in lines :

            line.budget_line_state = 'submit'


    def action_approve(self):

        approval_line = self.approval_line.search([('budget_id','=',self.id)])

        approved_lines = approval_line.mapped('state')

        if 'pending' in approved_lines : 

            app = approval_line.search([('name','=',self.env.user.id),('state','=','pending')],limit=1)

            self.write({'approval_line' :(1,app.id,{'state': 'approved','approval_time' : datetime.now(),'budget_id':self.id})})
          

        else :

            self.state = 'approved'

    def action_reject(self):

        self.write ({'state' : 'draft'})

class BudgetElements(models.Model):
    _name = 'budget.line'
    _description = 'Budget Elements'
    _inherit = [ 'mail.thread']

    
    name = fields.Char('Name' , required="1")
    state = fields.Selection(selection=[('draft','Draft'),('in_progress','In Progress'),('pending','Pending Approval'),('approved','approved'),], related='budget_id.state')

    currency_id = fields.Many2one('res.currency',string='Company Currency',default=lambda self: self.env.company.currency_id)
    cost = fields.Monetary()
    cost_by_company_currency = fields.Monetary()
    description = fields.Text()
    budget_id = fields.Many2one('budget' ,   required=1)
    category_id = fields.Many2one('category')
    company_id = fields.Many2one('res.company',name="Company",related='budget_id.company_id', store=True)
    department = fields.Many2one('department',related='budget_id.department',store=True)
    duration_from = fields.Date()
    duration_to = fields.Date()
    quarter = fields.Selection(selection=[('q1','Q1'),('q2','Q2'),('q3','Q3'),('q4','Q4')],default='q1')
    business_company_id = fields.Many2one('res.company',name="Related Company",)
    business_department = fields.Many2one('department', name = "Related Department")
    company_currency_id = fields.Many2one('res.currency' , related='company_id.currency_id',store='True')
    budget_line_state = fields.Selection(selection=[('draft','Draft'),('submit','submitted'),('pending','Pending Modifications')], default='draft' ,  tracking=True)
    justification = fields.Char()
    reject_reason = fields.Char()
    budget_type = fields.Selection(related="budget_id.budget_type",selection=[('it_budget','IT Budget'),('other','Non IT Department')])




    def action_submit(self):

        mail_template = self.env['mail.template'].search([('model_id','=','budget.line'),('name','=','Budget demand is submitted')])
        if mail_template : 
            mail_template.send_mail(self.id, force_send=True)

        self.write({'budget_line_state' : 'submit'})


    # @api.depends('cost')
    # def _cost_by_company_currency(self):
    #     if self.currency_id and self.company_id : 
    #         for record in self : 
    #             cost_by_company_currency = record.currency_id._convert(
    #                     abs(record.cost),
    #                     record.company_id.currency_id,
    #                     record.company_id,
    #                     datetime.today())
    #             record.cost_by_company_currency = cost_by_company_currency
                    


    @api.onchange('business_company_id')
    def get_business_department(self):
        if self.business_company_id is True:
            domain = [('company', '=', self.business_company_id.id)]
        else:
            domain = []
        return {'domain': {'business_department': domain}}


class ApprovalLine(models.Model):
    _name = 'approval.line'


    name = fields.Many2one('res.users')

    state = fields.Selection([('approved','Approved'),('pending','Pending Approval')],default='pending')

    budget_id = fields.Many2one('budget')

    approval_time = fields.Datetime()


class RejectBudgetLineWizard(models.TransientModel):
    _name = 'reject.budget.line.wizard'
    _description = 'Reject Wizard'


    name = fields.Char('Reasons to Reject')
    budget_line_id = fields.Many2one('budget.line')

    def action_reject(self):

        self.ensure_one()
        
        line = self.env['budget.line'].search([('id','=',self.budget_line_id.id)])

        line.sudo().write({'budget_line_state':'pending','reject_reason':self.name})

        mail_template = self.env['mail.template'].sudo().search([('model_id','=','budget.line'),('name','=','Budget demand is Rejected')])

        if mail_template : 
            mail_template.send_mail(line.id, force_send=True)


class RejectBudgetWizard(models.TransientModel):
    _name = 'reject.budget.wizard'
    _description = 'Reject Wizard'


    name = fields.Char('Reasons to Reject')
    budget_id = fields.Many2one('budget')

    def action_reject(self):

        self.ensure_one()
        
        budget = self.env['budget'].sudo().search([('id','=',self.budget_id.id)])


        budget.state = 'draft'

        budget.reject_reason = self.name

        mail_template = self.env['mail.template'].sudo().search([('model_id','=','budget'),('name','=','Budget is Rejected')])

        if mail_template :
            mail_template.send_mail(self.id, force_send=True)


# class Approvals(models.Model):
#     _name = 'budget.approval'

#     _order = "sequence,id"

#     name = fields.Many2one('res.users')
#     department = fields.Many2one('department',related='name.uasg_department')
#     description = fields.Text()
#     sequence = fields.Integer(default=10)


