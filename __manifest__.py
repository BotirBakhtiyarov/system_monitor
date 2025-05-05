{
    'name': 'System Monitor',
    'version': '1.0',
    'summary': 'System Monitoring Integration',
    'sequence': 10,
    'description': "Integration with system monitoring agent",
    'category': 'Tools',
    'author':'Nick',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/computer_views.xml',
        'views/metrics_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}