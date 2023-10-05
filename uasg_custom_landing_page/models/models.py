from odoo import models ,fields , api


class LandingPage(models.Model):
    
    _name="landing.page"

    _description = "Landing Page"


    name = fields.Char()

    user_id = fields.Many2one('res.users',compute='get_current_user')

    count_all_projects = fields.Integer(default=0,compute='get_all_projects')

    count_pipline = fields.Integer(default=0,compute='get_all_pipeline')

    count_completed = fields.Integer(default=0,compute='get_all_completed')

    count_in_progress = fields.Integer(default=0,compute='get_all_in_progress')



    def get_current_user(self):

        for record in self :

            record.user_id = self.env.user

    @api.depends('user_id')
    def get_all_projects(self):

        for record in self :

            assigned_projects = record.env['uasg.project'].search_count([('assigned_to','=',record.user_id.id)])

            record.count_all_projects = assigned_projects

    @api.depends('user_id')
    def get_all_pipeline(self):

        for record in self :

            assigned_projects = record.env['uasg.project'].search_count([('assigned_to','=',record.user_id.id),('status','=','pipeline')])

            record.count_pipline = assigned_projects


    @api.depends('user_id')
    def get_all_completed(self):

        for record in self :

            assigned_projects = record.env['uasg.project'].search_count([('assigned_to','=',record.user_id.id),('status','=','completed')])

            record.count_completed = assigned_projects

    @api.depends('user_id')
    def get_all_in_progress(self):

        for record in self :

            assigned_projects = record.env['uasg.project'].search_count([('assigned_to','=',record.user_id.id),('status','=','in_progress')])

            record.count_in_progress = assigned_projects