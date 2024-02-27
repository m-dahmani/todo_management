from odoo import models, fields


class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Todo Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    task_name = fields.Char(required=1, tracking=1)
    description = fields.Text(tracking=1)
    due_date = fields.Date(tracking=1)

    assign_to_id = fields.Many2one('res.partner')

    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='new')