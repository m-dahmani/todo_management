from odoo import models, fields, api
from odoo.exceptions import ValidationError


class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Task Name', required=1, tracking=1)
    description = fields.Text(tracking=1)
    due_date = fields.Date(default=fields.Date.today(), tracking=1)
    is_late = fields.Boolean()
    assign_to_id = fields.Many2one('res.partner')
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('close', 'Close'),
    ], default='new')

    timer_estimated = fields.Float("Estimated Time")
    line_ids = fields.One2many(comodel_name='task.line', inverse_name='task_id')
    active = fields.Boolean(default=True)
    timer_total = fields.Float('Total Time', compute='_compute_timer_total', store=1)

    @api.depends('timer_estimated', 'line_ids.timer')
    def _compute_timer_total(self):
        for rec in self:
            # calculate the sum of timer of all lines linked to the task (task_id)
            total_times = sum(rec.line_ids.mapped('timer'))
            rec.timer_total = total_times

    @api.constrains('timer_total')
    def _check_exceed_estimated_time(self):
        for rec in self:
            if rec.timer_total > rec.timer_estimated:
                raise ValidationError('Total times exceed estimated time')

    @api.onchange('timer_estimated', "timer_total")
    def _onchange_less_than_estimated_time(self):
        for rec in self:
            if rec.timer_total < rec.timer_estimated:
                warning = {
                    "title": "Warning",
                    "message": "Total times less than estimated time",
                    "type": "notification",
                }
                return {"warning": warning}

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
            if rec.due_date < fields.Date.today() and rec.state in ['new', 'in_progress']:
                rec.is_late = True


class TaskLine(models.Model):
    _name = 'task.line'

    task_id = fields.Many2one('todo.task')
    # date = fields.Date(related='task_id.due_date', string="Date", readonly=0)
    date = fields.Date(default=fields.Date.today(), string="Date")
    description = fields.Char()
    timer = fields.Float('Time')
