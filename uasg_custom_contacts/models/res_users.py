from odoo import models, fields, api



class ResUsers(models.Model):
    
    _inherit="res.users"

    
    uasg_contact = fields.Many2one('uasg.contacts',compute='_link_with_uasg_contacts')
    uasg_department = fields.Char(related='uasg_contact.department')
    


    @api.depends('login')
    def _link_with_uasg_contacts (self) :

        for record in self :
            user = record.env['uasg.contacts'].search([('email','=',record.login)],limit=1)
            if user :     
                    record.uasg_contact  = user.id
                    # if user.company_id :
                    #     record.company_id =user.company_id.id
                    # else :
                    #     record.company_id  = False
            else :
                record.uasg_contact = False

        return True

    # @api.onchange('uasg_contact')
    # def _link_with_company_id(self):

    #     for record in self :

    #         if record.uasg_contact : 

    #             record.company_id = record.uasg_contact.company_id.id


    # @api.constrains('company_id', 'company_ids', 'active')
    # def _check_company(self):
    #     for user in self.filtered(lambda u: u.active):
                
    #         if user.uasg_contact : 

    #             user.company_id = user.uasg_contact.company_id.id

    #         if user.company_id not in user.company_ids:
    #             user.company_ids = [4, user.company_id.id]
    #             return True
