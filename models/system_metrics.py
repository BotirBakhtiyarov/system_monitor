from odoo import models, fields, api


class Computer(models.Model):
    _name = 'system.monitor.computer'
    _description = 'Monitored Computer'

    name = fields.Char(string='Computer ID', required=True)
    username = fields.Char(string='Username')
    active = fields.Boolean(string='Active', default=True)
    last_seen = fields.Datetime(string='Last Seen')
    metric_ids = fields.One2many('system.monitor.metric', 'computer_id', string='Metrics')
    latest_cpu = fields.Float(compute='_compute_latest_metrics', string='Latest CPU %')
    latest_ram = fields.Float(compute='_compute_latest_metrics', string='Latest RAM %')

    def _compute_latest_metrics(self):
        for computer in self:
            latest_metric = self.env['system.monitor.metric'].search([
                ('computer_id', '=', computer.id)
            ], order='timestamp DESC', limit=1)
            computer.latest_cpu = latest_metric.cpu_percent or 0.0
            computer.latest_ram = latest_metric.ram_percent or 0.0


class SystemMetric(models.Model):
    _name = 'system.monitor.metric'
    _description = 'System Metrics'
    _order = 'timestamp desc'

    computer_id = fields.Many2one('system.monitor.computer', string='Computer', required=True)
    timestamp = fields.Datetime(string='Timestamp', required=True)
    cpu_percent = fields.Float(string='CPU %', digits=(5, 2))
    ram_total = fields.Float(string='Total RAM (MB)')
    ram_used = fields.Float(string='Used RAM (MB)')
    ram_percent = fields.Float(string='RAM %', digits=(5, 2))
    app_ids = fields.One2many('system.monitor.app', 'metric_id', string='Applications')


class ApplicationUsage(models.Model):
    _name = 'system.monitor.app'
    _description = 'Application Usage'

    metric_id = fields.Many2one('system.monitor.metric', string='Metric', required=True)
    name = fields.Char(string='Application', required=True)
    duration = fields.Integer(string='Duration (s)')
    cpu_usage = fields.Float(string='CPU %', digits=(5, 2))
    ram_usage = fields.Float(string='RAM %', digits=(5, 2))