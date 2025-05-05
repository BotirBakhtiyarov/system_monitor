from odoo import http
import json
from datetime import datetime


class MetricsController(http.Controller):
    @http.route('/api/data', type='json', auth='none', methods=['POST'], csrf=False)
    def handle_metrics(self, **kwargs):
        data = json.loads(http.request.httprequest.data)

        Computer = http.request.env['system.monitor.computer']
        Metric = http.request.env['system.monitor.metric']
        App = http.request.env['system.monitor.app']

        # Find or create computer
        computer = Computer.sudo().search([
            ('name', '=', data['computer_id'])
        ], limit=1)

        if not computer:
            computer = Computer.sudo().create({
                'name': data['computer_id'],
                'username': data['username']
            })

        # Update last seen
        computer.sudo().write({
            'last_seen': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

        # Create metric record
        metric = Metric.sudo().create({
            'computer_id': computer.id,
            'timestamp': datetime.fromisoformat(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
            'cpu_percent': data['cpu'],
            'ram_total': data['ram']['total'] / (1024 ** 2),  # Convert bytes to MB
            'ram_used': data['ram']['used'] / (1024 ** 2),
            'ram_percent': data['ram']['percent'],
        })

        # Create application records
        apps = []
        for app_name, app_data in data['apps'].items():
            apps.append({
                'metric_id': metric.id,
                'name': app_name,
                'duration': app_data['duration'],
                'cpu_usage': app_data['cpu'],
                'ram_usage': app_data['ram']
            })

        App.sudo().create(apps)

        return {'status': 'success'}