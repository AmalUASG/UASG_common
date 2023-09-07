# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime





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


    name = fields.Char('Project Name')
    description = fields.Text('Brief Description')
    assigned_to = fields.Many2one('res.users')
    vendor = fields.Many2one('vendors')
    status = fields.Selection(selection=[('completed','Completed'),('in_progress','In Progress'),('pipeline','Pipeline')], default='in_progress' , tracking=True)
    target_date = fields.Date()
    date = fields.Date(default=datetime.today())
    project_updates = fields.One2many('uasg.project.update' , 'project_id')
    tag_ids=fields.Many2many('project.tags', 'project_tags_rel','project_id','tag_id', string='Tags', help="Optional tags you may want to assign for custom reporting", ondelete='restrict')
    make_fields_read_only = fields.Boolean(compute='_make_fields_read_only' , tracking=True)

    def _make_fields_read_only(self) :

        user = self.env.user

        if user :

            if user.groups_id in ['group_project_manager'] :

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
