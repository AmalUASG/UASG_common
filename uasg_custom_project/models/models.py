# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError, ValidationError




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
    status = fields.Selection(selection=[('draft','Draft'),('in_progress','In Progress'),('pipeline','Pipeline'),('completed','Completed')], default='draft' , tracking=True)
    target_date = fields.Date(tracking=True)
    date = fields.Date(default=datetime.today(),tracking=True)
    project_updates = fields.One2many('uasg.project.update' , 'project_id',tracking=True)
    tag_ids=fields.Many2many('project.tags', 'project_tags_rel','project_id','tag_id', string='Tags', help="Optional tags you may want to assign for custom reporting", ondelete='restrict')
    make_fields_read_only = fields.Boolean(compute='_make_fields_read_only' , tracking=True , default=False)
    business_unit = fields.Many2one('res.company', tracking=True)
    requested_by = fields.Char(tracking=True)
    progress = fields.Selection(selection=[('in_progress','On track'),('off_track','Of track'),('done','Done')], default='in_progress' ,compute='_compute_progress' ,tracking=True)

    def _compute_progress(self) :
        for record in self : 

            if self.target_date :
                if record.target_date <= fields.Date.today() : 
                    if record.status == 'completed' :
                        record.progress ='done'
                    else :
                        record.progress = 'off_track'
                elif record.target_date >= fields.Date.today() and record.status =='completed' :
                    record.progress ='done'
                else :
                    record.progress  = 'in_progress'

    @api.constrains('target_date')
    def _check_target_date(self):

        if self.target_date :
            if self.target_date <= self.date:
                raise ValidationError('Target date must be before the start date.')    

    def action_submit(self):

        mail_template = self.env['mail.template'].search([('model_id','=','uasg.project'),('name','=','Project is submitted')])
        if mail_template : 
            mail_template.send_mail(self.id, force_send=True)

        self.write ({'status' : 'in_progress'})

    def action_pipeline(self):

        self.write ({'status' : 'pipeline'})


    def action_completed(self):

        self.write ({'status' : 'completed'})

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