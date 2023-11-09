
from werkzeug import urls
import logging

from odoo import api, fields, models, _




class UasgContacts(models.Model):
    _name = 'uasg.contacts'

    name = fields.Char()
    uasg_id = fields.Char()
    email = fields.Char()
    mobile = fields.Char()
    #odoo_groups = fields.mayny
    company = fields.Char()
    department = fields.Char()
    job_title= fields.Char()
    user = fields.Many2one('res.users' , compute = '_link_with_res_users' , store=True)

    @api.depends('email')
    def _link_with_res_users (self) :

        for record in self :
            user = record.env['res.users'].search([])
            for u in user :
                if u.email == record.email :
                    record.user  = u.id
        return True




# class GroupMembers(models.Model) :

#     _name = 'group.members'

#     name = fields.Char()
#     email = fields.Char()
#     group_id = fields.Many2one('uasg.groups' , ondelete='cascade')
#     user = fields.Many2one('res.users' , compute = '_link_with_res_users' , store=True)

#     @api.depends('email')
#     def _link_with_res_users (self) :

#         for record in self :
#             user = record.env['res.users'].search([])
#             for u in user :
#                 if u.email == record.email :
#                     record.user  = u.id
#         return True

