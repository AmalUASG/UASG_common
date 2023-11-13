from odoo import models, fields, api



class ResUsers(models.Model):
    
    _inherit="res.users"

    
    uasg_contact = fields.Many2one('uasg.contacts',compute='_link_with_uasg_contacts')
    uasg_department = fields.Char(related='uasg_contact.department')

    @api.depends('login')
    def _link_with_uasg_contacts (self) :

    	for record in self :
            user = record.env['uasg.contacts'].search([('email','=',record.login)])
            if user :     
                    record.uasg_contact  = user.id
            else :
                record.uasg_contact  = False
                