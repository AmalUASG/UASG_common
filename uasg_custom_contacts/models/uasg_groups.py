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
    #odoo_groups = fields.mayny
    company = fields.Char(compute='_update_user_company' )
    department = fields.Char(compute ='_update_user_depatment' )
    job_title= fields.Char()
    user = fields.Many2one('res.users' , compute = '_link_with_res_users' , store=True )
    # company_id = Many2one('res.company' , compute = '_link_with_res_company' , store=True)
    manager_name  = fields.Char(compute ='_get_user_manager' )
    manager_email = fields.Char(compute ='_get_user_manager' )
    company_id = fields.Many2one('res.company',compute='_get_res_company')
    

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

    @api.depends('uasg_id')
    def _update_user_depatment (self):

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

            get_user_department = str('https://graph.microsoft.com/v1.0/users/'+str(contact.uasg_id)+'/department')

            response_department = requests.request("GET" , get_user_department,headers=headers)

            
            if response_department.json().get('value') : 

                department = response_department.json().get('value')

                contact.write({'department' : department})

            else :

                contact.write({'department' : ""})

    @api.depends('uasg_id')
    def _update_user_company (self):

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

            get_user_company = str('https://graph.microsoft.com/v1.0/users/'+str(contact.uasg_id)+'/companyName')

            response_company = requests.request("GET" , get_user_company,headers=headers)

            
            if response_company.json().get('value') : 

                company = response_company.json().get('value')

                contact.write({'company' : company})

            else :

                contact.write({'company' : ""})





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

