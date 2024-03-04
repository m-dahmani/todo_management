from odoo import models, fields


class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Task Name', required=1, tracking=1)
    description = fields.Text(tracking=1)
    due_date = fields.Date(tracking=1)
    assign_to_id = fields.Many2one('res.partner')
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='new')

    def action_new(self):
        for rec in self:
            rec.write({'state': 'new'})

    def action_in_progress(self):
        for rec in self:
            rec.write({
                'state': 'in_progress'
            })

    def action_completed(self):
        for rec in self:
            rec.write({
                'state': 'completed'
            })
