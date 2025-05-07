{
    'name': 'System Monitor',
    'version': '2.0',
    'summary': 'Advanced System Monitoring Integration',
    'sequence': 10,
    'description': """
        Advanced system monitoring module for tracking computer metrics and application usage.
        Features:
        - Real-time system metrics collection
        - Computer activity tracking
        - Application usage monitoring
        - Comprehensive visualization dashboards
    """,
    'category': 'Tools',
    'author': 'Nick',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/computer_views.xml',
        'views/metrics_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}