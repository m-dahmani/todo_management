from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Task Name', required=1, tracking=1)
    description = fields.Text(tracking=1)
    due_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    assign_to_id = fields.Many2one('res.partner')
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('close', 'Close')
    ], default='new')

    timer_estimated = fields.Float("Estimated Time")
    line_ids = fields.One2many(comodel_name='task.line', inverse_name='task_id')
    active = fields.Boolean(default=True)

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

    def action_close(self):
        for rec in self:
            rec.write({
                'state': 'close'
            })

    def check_due_date(self):
        task_ids = self.search([])
        for rec in task_ids:
            if rec.due_date < fields.date.today() and rec.state in ['new', 'in_progress']:
                rec.is_late = True



class TaskLine(models.Model):
    _name = 'task.line'

    task_id = fields.Many2one('todo.task')
    date = fields.Date(related='task_id.due_date', string="Date", readonly=0)
    description = fields.Char()
    timer = fields.Float('Time')
    timer_total = fields.Float('Total Time', compute='_compute_timer_total')

    @api.depends('timer', 'task_id.timer_estimated')
    def _compute_timer_total(self):
        for line in self:
            # calculate the sum of timer of all lines linked to the task (task_id)
            total_times = sum(line.task_id.line_ids.mapped('timer'))
            # Limit the value of timer_total to the value of timer_estimated if it exceeds this value
            line.timer_total = min(total_times, line.task_id.timer_estimated)

    @api.constrains('timer', 'task_id.timer_estimated')
    def _check_exceed_estimated_time(self):
        for line in self:
            total_times = sum(line.task_id.line_ids.mapped('timer'))
            if total_times > line.timer_total:
                raise ValidationError('Total times exceed estimated time')
