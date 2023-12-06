import requests
from odoo import models, fields, api
import datetime
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

 
    def get_contacts(self):



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
        get_members_url = str('https://graph.microsoft.com/v1.0/users?$select=displayName,mail,id,mobilePhone,jobTitle,companyName,department,accountEnabled&$expand=manager($levels=max;$select=displayName,mail)')
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

                    elif key == 'companyName' :
                        
                        created_member.write({'company' : member['companyName']})

                    elif key == 'department' :
                        
                        created_member.write({'department' : member['department']})

                    elif key == 'manager' :
                        
                        created_member.write({'manager_name' : member['manager']['displayName'],'manager_email' : member['manager']['mail']})
                    elif key == 'accountEnabled' :
                        
                        created_member.write({'active' : member['accountEnabled']})
               
                
       
        while (response.json().get('@odata.nextLink')) :

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

                            elif key == 'companyName' :
                                
                                created_member.write({'company' : member['companyName']})

                            elif key == 'department' :
                                
                                created_member.write({'department' : member['department']})

                            elif key == 'manager' :
                        
                                created_member.write({'manager_name' : member['manager']['displayName'],'manager_email' : member['manager']['mail']})
                            elif key == 'accountEnabled' :
                        
                                created_member.write({'active' : member['accountEnabled']})
               

                       
        self.contacts_created = True


    def update_contacts(self) :
        tenant_id = self.tenant_id
        client_id = self.client_id
        client_secret = self.client_secret
        contacts = self.env['uasg.contacts'].search([])
        contacts_uasg_ids = contacts.mapped('uasg_id')
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        payload = str('grant_type=client_credentials&client_secret='+str(client_secret)+'&client_id='+str(client_id)+'&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default')
        url = str("https://login.microsoftonline.com/"+str(tenant_id)+"/oauth2/v2.0/token")
        req = requests.request("POST" , url,headers=headers,data = payload)
        req = req.json()
        access_token = req.get('access_token')
        last_update_date = datetime.strptime(str(self.write_date)[:-7],'%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%dT%H:%M:%SZ")
        get_members_url = str('https://graph.microsoft.com/v1.0/users?$filter=onPremisesLastSyncDateTime ge ' + last_update_date +'&$select=displayName,mail,id,mobilePhone,jobTitle,companyName,department,accountEnabled&$expand=manager($levels=max;$select=displayName,mail)&$top=999')
        headers = {'Content-Type': 'application/json','Authorization' : access_token }
        response = requests.request("GET" , get_members_url,headers=headers)
        members=response.json().get('value')
        if members :
            for member in members :

                if member['id'] in contacts_uasg_ids :

                    for contact in contacts :

                        if contact.uasg_id == member['id']:

                            if member['displayName'] == contact.name :
                                True
                            else :
                                contact.write({'name' : member['displayName']})

                            if member['mail'] == contact.email :
                                True
                            else :
                                contact.write({'email' : member['mail']})

                            if member['id'] == contact.uasg_id :
                                True
                            else :
                                contact.write({'uasg_id' : member['id']})

                            if member['mobilePhone'] == contact.uasg_id :
                                True
                            else :
                                contact.write({'mobile' : member['mobilePhone']})

                            if member['jobTitle'] == contact.job_title :
                                True
                            else :
                                contact.write({'job_title' : member['jobTitle']})

                            if member['department'] == contact.department :
                                True
                            else :
                                contact.write({'department' : member['department']})
                            if member['manager']['displayName']:
                                if member['manager']['displayName'] == contact.manager_name :
                                    True
                                else :
                                    contact.write({'manager_name' : member['manager']['displayName']})
                                if member['manager']['mail'] == contact.manager_email :
                                    True
                                else :
                                    contact.write({'manager_email' : member['manager']['manager_email']})

                            if member['accountEnabled'] == contact.active :
                                True
                            else :
                                contact.write({'active' : member['accountEnabled']})
                else :

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

                            elif key == 'companyName' :
                                
                                created_member.write({'company' : member['companyName']})

                            elif key == 'department' :
                                
                                created_member.write({'department' : member['department']})

                            elif key == 'manager' :
                        
                                created_member.write({'manager_name' : member['manager']['displayName'],'manager_email' : member['manager']['mail']})
                            elif key == 'accountEnabled' :
                        
                                created_member.write({'active' : member['accountEnabled']})

       
        while (response.json().get('@odata.nextLink')) :
            # raise UserError(str(response.json().get('@odata.next_link')))

            get_members_url = str(response.json().get('@odata.nextLink'))
            if get_members_url :
                response = requests.request("GET" , get_members_url,headers=headers)
                members=response.json().get('value')
                if members :

                    for member in members :

                        if member['id'] in contacts_uasg_ids :

                            for contact in contacts :

                                if contact.uasg_id == member['id']:

                                    if member['displayName'] == contact.name :
                                        True
                                    else :
                                        contact.write({'name' : member['displayName']})

                                    if member['mail'] == contact.email :
                                        True
                                    else :
                                        contact.write({'email' : member['mail']})

                                    if member['id'] == contact.uasg_id :
                                        True
                                    else :
                                        contact.write({'uasg_id' : member['id']})

                                    if member['mobilePhone'] == contact.uasg_id :
                                        True
                                    else :
                                        contact.write({'mobile' : member['mobilePhone']})

                                    if member['jobTitle'] == contact.job_title :
                                        True
                                    else :
                                        contact.write({'job_title' : member['jobTitle']})

                                    if member['jobTitle'] == contact.job_title :
                                        True
                                    else :
                                        contact.write({'job_title' : member['jobTitle']})

                                    if member['department'] == contact.department :
                                        True
                                    else :
                                        contact.write({'department' : member['department']})

                                    if member['manager']:
                                        if member['manager']['displayName'] == contact.manager_name :
                                            True
                                        else :
                                            contact.write({'manager_name' : member['manager']['displayName']})
                                        if member['manager']['mail'] == contact.manager_email :
                                            True
                                        else :
                                            contact.write({'manager_email' : member['manager']['mail']})


                                    if member['accountEnabled'] == contact.active :
                                        True
                                    else :
                                        contact.write({'active' : member['accountEnabled']})

                        else :

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

                                elif key == 'companyName' :
                                    
                                    created_member.write({'company' : member['companyName']})

                                elif key == 'department' :
                                    
                                    created_member.write({'department' : member['department']})

                                elif key == 'manager' :
                            
                                    created_member.write({'manager_name' : member['manager']['displayName'],'manager_email' : member['manager']['mail']})
                                elif key == 'accountEnabled' :
                            
                                    created_member.write({'active' : member['accountEnabled']})