# -*- coding: utf-8 -*-
# from odoo import http


# class UasgCustomBudget(http.Controller):
#     @http.route('/uasg_custom_budget/uasg_custom_budget', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/uasg_custom_budget/uasg_custom_budget/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('uasg_custom_budget.listing', {
#             'root': '/uasg_custom_budget/uasg_custom_budget',
#             'objects': http.request.env['uasg_custom_budget.uasg_custom_budget'].search([]),
#         })

#     @http.route('/uasg_custom_budget/uasg_custom_budget/objects/<model("uasg_custom_budget.uasg_custom_budget"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('uasg_custom_budget.object', {
#             'object': obj
#         })
