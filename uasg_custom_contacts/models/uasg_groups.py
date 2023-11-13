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
    manager_name  = fields.Char(compute ='_get_user_manager' , store=True )
    manager_email = fields.Char(compute ='_get_user_manager' ,store=True)
    company_id = fields.Many2one('res.company',compute='_get_res_company')


    @api.depends('company')
    def _get_res_company(self):

        for record in self :

            uasg_companies = record.env['uasg.company'].search([('name','=', record.company)],limit=1)

            if uasg_companies :

                record.company_id = uasg_companies.company_id.id

            else :

                record.company_id = False


    @api.depends('uasg_id')
    def _get_user_manager(self):

        config = self.env['ad.configuration'].search([('active','=',True)],limit=1)

        tenant_id = config.tenant_id
        client_id = config.client_id
        client_secret = config.client_secret
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        payload = str('grant_type=client_credentials&client_secret='+str(client_secret)+'&client_id='+str(client_id)+'&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default')
        url = str("https://login.microsoftonline.com/"+str(tenant_id)+"/oauth2/v2.0/token")
        req = requests.request("POST" , url,headers=headers,data = payload)
        req = req.json()
        access_token = req.get('access_token')
        headers = {'Content-Type': 'application/json','Authorization' : access_token }

        for contact in self :

            get_user_manager = str('https://graph.microsoft.com/v1.0/users/'+str(contact.uasg_id)+'/Manager')

            response_manager = requests.request("GET" , get_user_manager,headers=headers)
            
            if response_manager : 

                contact.write({'manager_name' : response_manager.json().get('displayName'),'manager_email' : response_manager.json().get('mail')})

            else :

                contact.write({'manager_name' : "-",'manager_email' : "-"})



    @api.depends('email')
    def _link_with_res_users (self) :

        for record in self :
            user = record.env['res.users'].search([])
            for u in user :
                if u.email == record.email :
                    record.user  = u.id
                else :
                    return True
