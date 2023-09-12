# -*- coding: utf-8 -*-
# from odoo import http


# class UasgCustomProject(http.Controller):
#     @http.route('/uasg_custom_project/uasg_custom_project', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/uasg_custom_project/uasg_custom_project/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('uasg_custom_project.listing', {
#             'root': '/uasg_custom_project/uasg_custom_project',
#             'objects': http.request.env['uasg_custom_project.uasg_custom_project'].search([]),
#         })

#     @http.route('/uasg_custom_project/uasg_custom_project/objects/<model("uasg_custom_project.uasg_custom_project"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('uasg_custom_project.object', {
#             'object': obj
#         })
