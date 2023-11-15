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
        get_members_url = str('https://graph.microsoft.com/v1.0/users?$filter=accountEnabled%20eq%20true&$select=displayName,mail,id,mobilePhone,jobTitle,companyName,department')
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

                            elif key == 'companyName' :
                                
                                created_member.write({'company' : member['companyName']})

                            elif key == 'department' :
                                
                                created_member.write({'department' : member['department']})


                       
        self.contacts_created = True


    def update_contacts(self) :


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

        last_update_date = datetime.strptime(str(self.write_date)[:-7],'%Y-%m-%dT%H:%M:%Sz')
        get_members_url = str('https://graph.microsoft.com/v1.0/users?$filter=accountEnabled%20eq%20true&onPremisesLastSyncDateTime ge' + last_update_date +'&$select=displayName,mail,id,mobilePhone,jobTitle,companyName,department&$top=999')
        raise UserError(str(get_members_url))
        headers = {'Content-Type': 'application/json','Authorization' : access_token }
        response = requests.request("GET" , get_members_url,headers=headers)
        members=response.json().get('value')
        if members :
            for member in members :

                for key in member : 

                    for contact in contacts : 

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

                            elif key == 'companyName' :
                                
                                created_member.write({'company' : member['companyName']})

                            elif key == 'department' :
                                
                                created_member.write({'department' : member['department']})


