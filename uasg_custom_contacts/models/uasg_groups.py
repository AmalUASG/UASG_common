import requests
from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
import logging



class UasgContacts(models.Model):
    _name = 'uasg.contacts'

    name = fields.Char()
    uasg_id = fields.Char()
    email = fields.Char()
    mobile = fields.Char()
    company = fields.Char()
    department = fields.Char( )
    job_title= fields.Char()
    manager_name  = fields.Char()
    manager_email = fields.Char()
    company_id = fields.Many2one('res.company',compute='_get_res_company')
    active = fields.Boolean()


    @api.depends('company')
    def _get_res_company(self):

        for record in self :

            uasg_companies = record.env['uasg.company'].search([('name','=', record.company)],limit=1)

            if uasg_companies :

                record.company_id = uasg_companies.company_id.id

            else :

                record.company_id = False

    @api.depends('email')
    def _link_with_res_users (self) :

        for record in self :
            user = record.env['res.users'].search([])
            for u in user :
                if u.email == record.email :
                    record.user  = u.id
                else :
                    return True
