from odoo import models, fields, api



class ResUsers(models.Model):
    
    _inherit="res.user"


    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company.id,
        help='The default company for this user.', context={'user_preference': True})