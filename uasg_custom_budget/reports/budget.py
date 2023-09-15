
from odoo import fields, models, tools

from odoo.addons.rating.models.rating_data import RATING_LIMIT_MIN, RATING_TEXT

class ReportBudget(models.Model):
    _name = "report.reportbudget"
    _description = "Budget Analysis"
    _order = 'name desc, budget_id'
    _auto = False

    name = fields.Char(string='Item', readonly=True)
    duration_from = fields.Datetime(string='From', readonly=True)
    duration_to = fields.Datetime(string='To', readonly=True)
    budget_id = fields.Many2one('budget', string='Budget', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    department = fields.Many2one('department')
    cost = fields.Float()

    # stage_id = fields.Many2one('project.task.type', string='Stage', readonly=True)
    # is_closed = fields.Boolean("Closing Stage", readonly=True, help="Folded in Kanban stages are closing stages.")
    # task_id = fields.Many2one('project.task', string='Tasks', readonly=True)
    # active = fields.Boolean(readonly=True)

    # parent_id = fields.Many2one('project.task', string='Parent Task', readonly=True)
    # ancestor_id = fields.Many2one('project.task', string="Ancestor Task", readonly=True)
    # # We are explicitly not using a related field in order to prevent the recomputing caused by the depends as the model is a report.
    # rating_last_text = fields.Selection(RATING_TEXT, string="Rating Last Text", compute="_compute_rating_last_text", search="_search_rating_last_text")
    # personal_stage_type_ids = fields.Many2many('project.task.type', relation='project_task_user_rel',
    #     column1='task_id', column2='stage_id',
    #     string="Personal Stage", readonly=True)
    # milestone_id = fields.Many2one('project.milestone', readonly=True)
    # milestone_reached = fields.Boolean('Is Milestone Reached', readonly=True)
    # milestone_deadline = fields.Date('Milestone Deadline', readonly=True)

    


    def _select(self):
        return """
                (select 1) AS nbr,
                t.id as id,
                t.id as budget_id,
                t.active,
                t.duration_from as duration_from,
                t.duration_to as duration_to,
            
                t.name as name,
                t.company_id,

        """

    def _group_by(self):
        return """
                t.id,
                t.company_id,
               
        """

    def _from(self):
        return f"""

        budget
                # project_task t
                #     LEFT JOIN rating_rating rt ON rt.res_id = t.id
                #         AND rt.res_model = 'project.task'
                #         AND rt.consumed = True
                #         AND rt.rating >= {RATING_LIMIT_MIN}
                #     LEFT JOIN project_milestone pm ON pm.id = t.milestone_id
        """

    def _where(self):
        return """
                t.budget_id IS NOT NULL
        """

    # def init(self):
    #     tools.drop_view_if_exists(self._cr, self._table)
    #     self._cr.execute("""
    # CREATE view %s as
    #      SELECT %s
    #       WHERE %s
    #    GROUP BY %s
    #     """ % (self._table, self._select(), self._from(), self._where(), self._group_by()))
