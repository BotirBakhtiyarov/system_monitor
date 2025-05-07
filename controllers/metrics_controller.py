from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError
import json
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class MetricsController(http.Controller):
    @http.route('/api/data', type='json', auth='public', methods=['POST'], csrf=False)
    def handle_metrics(self, **kwargs):
        """
        Handle incoming system metrics data.
        Expects JSON payload with computer metrics and application usage.
        """
        try:
            # Parse incoming data
            data = json.loads(request.httprequest.data.decode('utf-8'))
            if not data.get('computer_id') or not data.get('timestamp'):
                return {'status': 'error', 'message': 'Missing required fields'}

            # Initialize models
            Computer = request.env['system.monitor.computer'].sudo()
            Metric = request.env['system.monitor.metric'].sudo()
            App = request.env['system.monitor.app'].sudo()

            # Find or create computer
            computer = Computer.search([('name', '=', data['computer_id'])], limit=1)
            if not computer:
                computer = Computer.create({
                    'name': data['computer_id'],
                    'username': data.get('username', ''),
                })

            # Update last seen
            computer.write({'last_seen': fields.Datetime.now()})

            # Create metric record
            metric = Metric.create({
                'computer_id': computer.id,
                'timestamp': datetime.fromisoformat(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                'cpu_percent': float(data.get('cpu', 0)),
                'ram_total': data.get('ram', {}).get('total', 0) / (1024 ** 2),
                'ram_used': data.get('ram', {}).get('used', 0) / (1024 ** 2),
                'ram_percent': float(data.get('ram', {}).get('percent', 0)),
            })

            # Create application records
            apps = []
            for app_name, app_data in data.get('apps', {}).items():
                apps.append({
                    'metric_id': metric.id,
                    'name': app_name,
                    'duration': int(app_data.get('duration', 0)),
                    'cpu_usage': float(app_data.get('cpu', 0)),
                    'ram_usage': float(app_data.get('ram', 0)) / (1024 ** 2),
                })
            if apps:
                App.create(apps)

            return {'status': 'success', 'message': 'Metrics recorded successfully'}

        except (ValueError, KeyError, TypeError) as e:
            _logger.error(f"Error processing metrics: {str(e)}")
            return {'status': 'error', 'message': f'Invalid data format: {str(e)}'}
        except Exception as e:
            _logger.exception("Unexpected error in metrics controller")
            return {'status': 'error', 'message': 'Internal server error'}