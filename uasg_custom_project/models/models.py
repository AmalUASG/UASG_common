# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
import requests
import json


class Users(models.Model):

    _inherit = 'res.partner'

    line_manager = fields.Many2one('res.users')

class Vendor(models.Model):
    
    _name="vendors"
    name = fields.Char()

class ProjectTag(models.Model):
    
    _name="project.tags"
    name = fields.Char()

    color = fields.Integer(string='Color Index')

class UASGProject(models.Model):
    _name = 'uasg.project'
    _description = 'Project'

    _inherit = [ 'mail.thread']


    name = fields.Char('Project Name' , tracking=True)
    description = fields.Text('Brief Description' , tracking=True)
    assigned_to = fields.Many2one('res.users' , tracking=True )
    vendor = fields.Many2one('vendors' , tracking=True)
    status = fields.Selection(selection=[('draft','Draft'),('pipeline','Pipeline'),('in_progress','In Progress'),('completed','Completed')], default='draft' , tracking=True)
    target_date = fields.Date(tracking=True)
    date = fields.Date(default=datetime.today(),tracking=True)
    project_updates = fields.One2many('uasg.project.update' , 'project_id',tracking=True)
    tag_ids=fields.Many2many('project.tags', 'project_tags_rel','project_id','tag_id', string='Tags', help="Optional tags you may want to assign for custom reporting", ondelete='restrict')
    make_fields_read_only = fields.Boolean(compute='_make_fields_read_only' , tracking=True , default=False)
    business_unit = fields.Many2one('res.company', tracking=True)
    requested_by = fields.Char(tracking=True)
    progress = fields.Selection(selection=[('in_progress','On track'),('off_track','Off track'),('done','Done')], default='in_progress' ,compute='_compute_progress' ,tracking=True)
    latest_update = fields.Text(compute='_compute_latest_update')
    reject_reason = fields.Char()
    company_id = fields.Many2one('res.company',name="Company",default=lambda self: self.env.company)
    needs_cost = fields.Boolean()
    currency_id = fields.Many2one('res.currency',related='company_id.currency_id')
    cost = fields.Monetary()



    @api.depends('project_updates')

    def _compute_latest_update(self) :
        for record in self :
            project_updates = record.env['uasg.project.update'].sudo().search([('project_id','=',record.id)])
            latest_update = ''
            if project_updates :

                for update in project_updates:

                    latest_update = update.name

            record.latest_update = latest_update


    def _compute_progress(self) :
        for record in self : 

            if record.target_date :
                if record.target_date <= fields.Date.today() : 
                    if record.status == 'completed' :
                        record.progress ='done'
                    else :
                        record.progress = 'off_track'
                elif record.target_date >= fields.Date.today() and record.status =='completed' :
                    record.progress ='done'
                else :
                    record.progress  = 'in_progress'
            else :
                record.progress = 'off_track'

    @api.constrains('target_date')
    def _check_target_date(self):

        if self.target_date :
            if self.target_date <= self.date:
                raise ValidationError('Target date must be before the start date.')    

    def action_submit(self):

        mail_template = self.env['mail.template'].search([('model_id','=','uasg.project'),('name','=','Project is submitted')])

        

        message = json.dumps({
          "message": {
            "subject": mail_template.subject,
            "body": {
              "contentType": "Html",
              "content": mail_template.body_html,
            },
            "toRecipients": [
              {
                "emailAddress": {
                  "address": mail_template.email_to
                }
              }
            ],
            "ccRecipients": [
              {
                "emailAddress": {
                  "address": mail_template.email_cc
                }
              }
            ]
          },
          "saveToSentItems": "true"
        })

        headers = {"Content-type": "application/x-www-form-urlencoded"}
        payload = str('grant_type=autherization_code&client_secret=vqM8Q~C8xLH55ysYRLKnYpW8.wFh100HVqukqdm3&client_id=2e98a997-764b-41e6-976f-4451a215e063'+'&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default')
        url = str("https://login.microsoftonline.com/58481125-7f09-407d-921a-dc425b00fd0f/oauth2/v2.0/token")
        req = requests.request("POST" , url,headers=headers,data = payload)
        req = req.json()
        access_token = req.get('access_token')
        url = "https://graph.microsoft.com/v1.0/me/sendMail"
        headers = {'Content-Type': 'application/json','Authorization' : access_token }
        response = requests.request("POST" , url,headers=headers,data=message)
        if response :

            raise UserError(str(response))

            # mail_template.send_mail(self.id, force_send=True)

        self.write ({'status' : 'pipeline'})

    def action_pipeline(self):

        if self.assigned_to.partner_id.line_manager == self.env.user :

            self.write ({'status' : 'in_progress'})
            
            mail_template = self.env['mail.template'].sudo().search([('model_id','=','uasg.project'),('name','=','Project has been Approved')])

            if mail_template :
                mail_template.send_mail(self.id, force_send=True)

        else :

            raise UserError('Sorry , Approval should be done by the Line Manager : ' + str(self.assigned_to.partner_id.line_manager.name))


    def action_completed(self):

        self.write ({'status' : 'completed'})

    def action_reopen(self):

        if self.assigned_to == self.env.user or self.assigned_to.partner_id.line_manager == self.env.user :

            self.write ({'status' : 'in_progress'})

            mail_template = self.env['mail.template'].sudo().search([('model_id','=','uasg.project'),('name','=','Project has been Re-opend')])

            if mail_template :
                mail_template.send_mail(self.id, force_send=True)
        else :

            raise UserError('Sorry , This Action is restricted to the Asignee/line Manager Only ! ')


    def action_draft(self):

        if self.assigned_to == self.env.user or self.assigned_to.partner_id.line_manager == self.env.user :

            self.write ({'status' : 'draft'})

            mail_template = self.env['mail.template'].sudo().search([('model_id','=','uasg.project'),('name','=','Project has been Drafted')])

            if mail_template :
                mail_template.send_mail(self.id, force_send=True)
        else :

            raise UserError('Sorry , This Action is restricted to the Asignee/line Manager Only ! ')
    def _make_fields_read_only(self) :

        user = self.env.user
        user_groups = self.env.user.groups_id
        groups = user_groups.mapped('full_name')



        if user and groups : 

            if 'UASG Project / Manager' in groups :

                self.make_fields_read_only = False

            else:

                self.make_fields_read_only = True


class ProjectUpdate(models.Model):
    _name = 'uasg.project.update'
    _description = 'Project Updates'


    name = fields.Text('update')
    date = fields.Date(default=datetime.today())
    project_id = fields.Many2one('uasg.project')
    implementation_dependancy = fields.Text()
    attachment_ids = fields.Many2many(
        comodel_name='ir.attachment',
        relation='budget_ir_attachments_rel',
        string='Attachments')

    @api.model
    def create(self, vals):
        templates = super(ProjectUpdate,self).create(vals)
            # fix attachment ownership
        for template in templates:
            if template.attachment_ids:
                template.attachment_ids.write({'res_model': self._name, 'res_id': template.id})
        return templates

class RejectProjectWizard(models.TransientModel):
    _name = 'reject.project.wizard'
    _description = 'Reject Wizard'


    name = fields.Char('Reasons to Reject')
    project_id = fields.Many2one('uasg.project')

    def action_reject(self):

        

        if self.project_id.assigned_to.partner_id.line_manager == self.env.user :

            project = self.env['uasg.project'].sudo().search([('id','=',self.project_id.id)])


            project.sudo().write({'status':'draft' , 'reject_reason' : self.name})

            mail_template = self.env['mail.template'].sudo().search([('model_id','=','uasg.project'),('name','=','Project is Rejected')])

            if mail_template :
                mail_template.send_mail(project.id, force_send=True)

        else :

            raise UserError("Sorry , Only the line Manager can do the Rejection")