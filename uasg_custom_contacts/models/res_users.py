from odoo import models, fields, api



class ResUsers(models.Model):
    
    _inherit="res.users"

    
    uasg_contact = fields.Many2one('uasg.contacts',compute='_link_with_uasg_contacts')
    uasg_department = fields.Char(related='uasg_contact.department')

    company_id = fields.Many2one('res.company', related="uasg_contact.company_id" , string='Company', required=True, default=lambda self: self.env.company.id,
        help='The default company for this user.', context={'user_preference': True})


    @api.depends('login')
    def _link_with_uasg_contacts (self) :

    	for record in self :
            user = record.env['uasg.contacts'].search([('email','=',record.login)],limit=1)
            if user :     
                    record.uasg_contact  = user.id
            else :
                record.uasg_contact  = False
