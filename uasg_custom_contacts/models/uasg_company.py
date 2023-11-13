from odoo import models, fields, api



class UasgCompanies(models.Model):
    
    _name="uasg.company"


    name = fields.Char()

    company_id = fields.Many2one('res.company')