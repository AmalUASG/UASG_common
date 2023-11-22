from odoo import models, fields, api



class UasgDeaprtments(models.Model):
    
    _name="uasg.department"

    name = fields.Char()

    uasg_company = fields.Many2one('uasg.company')

    company_id = fields.Many2one('res.company',related ='uasg_company.company_id')