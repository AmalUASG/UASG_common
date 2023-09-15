from odoo import http
from odoo.http import request, route


class UasgCustomBudget(http.Controller):

    @http.route('''/budget/approve/<model("budget"):budget>''', auth='user', type='http')
    def budget_approval(self, budget):

        budget = request.env['budget'].sudo().search([('id','=',budget.id)])
        values = {'budget' : budget}

        if budget.state not in ['pending','approved'] :

        	return request.render("uasg_custom_budget.pending", values)

        budget.sudo().write({'state' : 'approved' , 'note' : 'Approved By Email' })

        mail_template = request.env['mail.template'].sudo().search([('name','=','Budget is Approved')])
        if mail_template : 
            mail_template.send_mail(budget.id, force_send=True)


        return request.render("uasg_custom_budget.approved", values)



    @http.route('''/budget/reject/<model("budget"):budget>''', auth='user', type='http')
    def budget_reject(self, budget):

        budget = request.env['budget'].sudo().search([('id','=',budget.id)])
        values = {'budget' : budget}

        if budget.state not in ['pending','in_progress'] :

        	return request.render("uasg_custom_budget.pending", values)

        budget.sudo().write({'state' : 'in_progress' , 'note' : 'Rejected By Email'})
        mail_template = request.env['mail.template'].sudo().search([('name','=','Budget is Rejected')])
        if mail_template : 
            mail_template.send_mail(budget.id, force_send=True)

        return request.render("uasg_custom_budget.rejected", values)


    