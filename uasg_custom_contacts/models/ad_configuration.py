import requests
from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
import logging



DEFAULT_MICROSOFT_AUTH_ENDPOINT = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
DEFAULT_MICROSOFT_TOKEN_ENDPOINT = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
_logger = logging.getLogger(__name__)

TIMEOUT = 20

class AdConfiguration(models.Model):
    
    _name="ad.configuration"


    name = fields.Char(required=1)
    tenant_id = fields.Char(required=1)
    client_id = fields.Char(required=1)
    client_secret = fields.Char(required=1)
    active = fields.Boolean()
    contacts_created = fields.Boolean(default=False)

    @api.constrains('active')

    def _check_active(self):

        checked_bool = self.search([('id', '!=', self.id),('active', '=', True)], limit=1)  
        if self.active and checked_bool:
            raise ValidationError(("There's already an active configuration for Microsoft AD , deactivate it and try again  '%s'") % checked_bool.name)

    @api.model
    def _get_token_endpoint(self):
        return self.env["ir.config_parameter"].sudo().get_param('microsoft_account.token_endpoint', DEFAULT_MICROSOFT_TOKEN_ENDPOINT)

    # def get_groups(self):

    #     if self.active & self.groups_created == False : 
        
    #         tenant_id = self.tenant_id
    #         client_id = self.client_id
    #         client_secret = self.client_secret


    #         headers = {"Content-type": "application/x-www-form-urlencoded"}
    #         payload = str('grant_type=client_credentials&client_secret='+str(client_secret)+'&client_id='+str(client_id)+'&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default')
    #         url = str("https://login.microsoftonline.com/"+str(tenant_id)+"/oauth2/v2.0/token")
    #         req = requests.request("POST" , url,headers=headers,data = payload)
    #         req = req.json()
    #         access_token = req.get('access_token')
    #         groups_url = str('https://graph.microsoft.com/v1.0/financials/companies/?$top=999')
    #         headers = {'Content-Type': 'application/json','Authorization' : access_token }


    #         groups = requests.request("GET" , groups_url,headers=headers)


    #         groups=groups.json().get('value')

    #         raise ValidationError(str(groups))

    #         for i in groups :

    #             a = self.env['uasg.groups'].create({})
    #             for key in i :
        
    #                 if key == 'id' :
    #                     a.write({'uasg_id' : i[key]})
    #                 if key == 'mail' :
    #                     a.write({'mail' : i[key]}) 
    #                 if key == 'displayName' :
    #                     a.write({'name' : i[key]})
    #                 if key == 'description' : 
    #                     a.write({'description' : i[key]})                
    #         self.groups_created = True

    def get_contacts(self):

        # groups = self.env['uasg.groups'].search([])

        # if groups : 

        tenant_id = self.tenant_id
        client_id = self.client_id
        client_secret = self.client_secret
        contacts = self.env['uasg.contacts'].search([])



        headers = {"Content-type": "application/x-www-form-urlencoded"}
        payload = str('grant_type=client_credentials&client_secret='+str(client_secret)+'&client_id='+str(client_id)+'&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default')
        url = str("https://login.microsoftonline.com/"+str(tenant_id)+"/oauth2/v2.0/token")
        req = requests.request("POST" , url,headers=headers,data = payload)
        req = req.json()
        access_token = req.get('access_token')
        get_members_url = str('https://graph.microsoft.com/v1.0/users?$top=999')
        headers = {'Content-Type': 'application/json','Authorization' : access_token }
        response = requests.request("GET" , get_members_url,headers=headers)
        members=response.json().get('value')
        if members :
            for member in members :

                for key in member : 

                    if key == 'displayName' : 

                        created_member = contacts.create({'name':member['displayName'] })

                    elif key == 'mail' :
                        
                        created_member.write({'email' : member['mail']})

                    elif key == 'id' :
                        
                        created_member.write({'uasg_id' : member['id']})
                    elif key == 'mobilePhone' :
                        
                        created_member.write({'mobile' : member['mobilePhone']})
                    elif key == 'jobTitle' :
                        
                        created_member.write({'job_title' : member['jobTitle']})
                    
                

       
        while (response.json().get('@odata.nextLink')) :
            # raise UserError(str(response.json().get('@odata.next_link')))

            get_members_url = str(response.json().get('@odata.nextLink'))
            if get_members_url :
                response = requests.request("GET" , get_members_url,headers=headers)
                members=response.json().get('value')
                if members :
                    for member in members :

                        for key in member : 

                            if key == 'displayName' : 

                                created_member = contacts.create({'name':member['displayName'] })

                            elif key == 'mail' :
                                
                                created_member.write({'email' : member['mail']})

                            elif key == 'id' :
                                
                                created_member.write({'uasg_id' : member['id']})
                            elif key == 'mobilePhone' :
                                
                                created_member.write({'mobile' : member['mobilePhone']})
                            elif key == 'jobTitle' :

                                created_member.write({'job_title' : member['jobTitle']})

                       
        self.contacts_created = True

    def update_companies (self):

        tenant_id = self.tenant_id
        client_id = self.client_id
        client_secret = self.client_secret
        contacts = self.env['uasg.contacts'].search([])
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        payload = str('grant_type=client_credentials&client_secret='+str(client_secret)+'&client_id='+str(client_id)+'&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default')
        url = str("https://login.microsoftonline.com/"+str(tenant_id)+"/oauth2/v2.0/token")
        req = requests.request("POST" , url,headers=headers,data = payload)
        req = req.json()
        access_token = req.get('access_token')
        headers = {'Content-Type': 'application/json','Authorization' : access_token }


        for contact in contacts :

            get_user_company = str('https://graph.microsoft.com/v1.0/users/'+str(contact.uasg_id)+'/companyName')
            response_company = requests.request("GET" , get_user_company,headers=headers)
            if str(response_company.json().get('value')) != None : 
                raise UserError(str(response_company.json().get('value')))
                contact.write({'company' : str(response_company.json().get('value'))})






