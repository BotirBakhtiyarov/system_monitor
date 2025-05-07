from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class Computer(models.Model):
    _name = 'system.monitor.computer'
    _description = 'Monitored Computer'
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Computer ID must be unique.')
    ]

    name = fields.Char(string='Computer ID', required=True, index=True)
    username = fields.Char(string='Username')
    last_seen = fields.Datetime(string='Last Seen', index=True)
    metric_ids = fields.One2many('system.monitor.metric', 'computer_id', string='Metrics')
    latest_cpu = fields.Float(
        compute='_compute_latest_metrics',
        string='Latest CPU %',
        store=False
    )
    latest_ram = fields.Float(
        compute='_compute_latest_metrics',
        string='Latest RAM %',
        store=False
    )
    is_active = fields.Boolean(
        compute='_compute_is_active',
        string='Active Status',
        store=False
    )

    @api.depends('last_seen')
    def _compute_is_active(self):
        """Determine if computer is active (last seen within 5 minutes)."""
        now = fields.Datetime.now()
        for computer in self:
            computer.is_active = False
            if computer.last_seen:
                delta = now - computer.last_seen
                computer.is_active = delta.total_seconds() <= 300

    @api.depends('metric_ids', 'metric_ids.cpu_percent', 'metric_ids.ram_percent')
    def _compute_latest_metrics(self):
        """Compute latest CPU and RAM metrics."""
        for computer in self:
            latest_metric = self.env['system.monitor.metric'].search([
                ('computer_id', '=', computer.id)
            ], order='timestamp DESC', limit=1)
            computer.latest_cpu = latest_metric.cpu_percent or 0.0
            computer.latest_ram = latest_metric.ram_percent or 0.0

    @api.constrains('name')
    def _check_name(self):
        """Validate computer name format."""
        for computer in self:
            if not computer.name or len(computer.name.strip()) < 3:
                raise ValidationError('Computer ID must be at least 3 characters long.')

class SystemMetric(models.Model):
    _name = 'system.monitor.metric'
    _description = 'System Metrics'
    _order = 'timestamp DESC'
    _rec_name = 'timestamp'

    computer_id = fields.Many2one(
        'system.monitor.computer',
        string='Computer',
        required=True,
        index=True
    )
    timestamp = fields.Datetime(string='Timestamp', required=True, index=True)
    cpu_percent = fields.Float(string='CPU Usage %', digits=(5, 2))
    ram_total = fields.Float(string='Total RAM (MB)', digits=(10, 2))
    ram_used = fields.Float(string='Used RAM (MB)', digits=(10, 2))
    ram_percent = fields.Float(string='RAM Usage %', digits=(5, 2))
    app_ids = fields.One2many('system.monitor.app', 'metric_id', string='Applications')

    @api.constrains('cpu_percent', 'ram_percent')
    def _check_percentages(self):
        """Validate percentage values."""
        for metric in self:
            if not (0 <= metric.cpu_percent <= 100):
                raise ValidationError('CPU percentage must be between 0 and 100.')
            if not (0 <= metric.ram_percent <= 100):
                raise ValidationError('RAM percentage must be between 0 and 100.')

class ApplicationUsage(models.Model):
    _name = 'system.monitor.app'
    _description = 'Application Usage'
    _order = 'name'

    metric_id = fields.Many2one(
        'system.monitor.metric',
        string='Metric',
        required=True,
        index=True
    )
    name = fields.Char(string='Application', required=True, index=True)
    duration = fields.Integer(string='Duration (seconds)')
    cpu_usage = fields.Float(string='CPU Usage %', digits=(5, 2))
    ram_usage = fields.Float(string='RAM Usage (MB)', digits=(10, 2))

    @api.constrains('duration')
    def _check_duration(self):
        """Validate duration is non-negative."""
        for app in self:
            if app.duration < 0:
                raise ValidationError('Duration cannot be negative.')