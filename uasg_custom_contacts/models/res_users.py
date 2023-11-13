from odoo import models, fields, api



class ResUsers(models.Model):
    
    _inherit="res.user"

    
    uasg_contact = fields.Many2one('uasg.contacts',compute='_link_with_uasg_contacts')
    uasg_department = fields.Char(related='uasg_contact.department')


    def _link_with_uasg_contacts (self) :

    	for record in self :

            user = record.env['uasg.contacts'].search([])
            for u in user :
                if u.email == record.login :
                    record.uasg_contact  = u.id
                else :
                    return True