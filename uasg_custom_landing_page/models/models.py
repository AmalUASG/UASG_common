from odoo import models ,fields , api


class LandingPage(models.Model):
    
    _name="landing.page"

    _description = "Landing Page"


    name = fields.Char()

    user_id = fields.Many2one('res.users',compute='get_current_user')
    current_usag_contact = fields.Many2one('uasg.contact',related="user_id.uasg_contact")

    count_all_projects = fields.Integer(default=0,compute='get_all_projects')

    count_pipline = fields.Integer(default=0,compute='get_all_pipeline')

    count_completed = fields.Integer(default=0,compute='get_all_completed')

    count_in_progress = fields.Integer(default=0,compute='get_all_in_progress')

    uasg_department = fields.Char(related='user_id.uasg_department')


    def get_current_user(self):

        for record in self :

            record.user_id = self.env.user

    @api.depends('user_id')
    def get_all_projects(self):

        for record in self :

            assigned_projects = record.env['uasg.project'].search_count([('uasg_contact','=',self.env.user.uasg_contact.id)])

            record.count_all_projects = assigned_projects

    @api.depends('user_id')
    def get_all_pipeline(self):

        for record in self :

            assigned_projects = record.env['uasg.project'].search_count([('uasg_contact','=',self.env.user.uasg_contact.id),('status','=','pipeline')])

            record.count_pipline = assigned_projects


    @api.depends('user_id')
    def get_all_completed(self):

        for record in self :

            assigned_projects = record.env['uasg.project'].search_count([('uasg_contact','=',self.env.user.uasg_contact.id),('status','=','completed')])

            record.count_completed = assigned_projects

    @api.depends('user_id')
    def get_all_in_progress(self):

        for record in self :

            assigned_projects = record.env['uasg.project'].search_count([('uasg_contact','=',self.env.user.uasg_contact),('status','=','in_progress')])

            record.count_in_progress = assigned_projects
