# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class uasg_single_sign_on(models.Model):
#     _name = 'uasg_single_sign_on.uasg_single_sign_on'
#     _description = 'uasg_single_sign_on.uasg_single_sign_on'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
