# Odoo System Monitor Module

![Odoo Version](https://img.shields.io/badge/Odoo-17.0-blue)
![License](https://img.shields.io/badge/License-LGPL--3-green)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

The **System Monitor** module is an Odoo 17 module designed to monitor and track system metrics for computers, including CPU usage, RAM usage, and application activity. It provides a robust API endpoint to collect real-time metrics and offers comprehensive views (kanban, tree, form, graph, and pivot) for analyzing system performance.

## Features

- **Real-time Metrics Collection**: Collect CPU, RAM, and application usage data via a JSON API endpoint.
- **Computer Tracking**: Monitor individual computers with unique IDs, tracking their last seen status and activity.
- **Application Usage Monitoring**: Record application-specific metrics, including duration, CPU, and RAM usage.
- **Visualization Dashboards**:
  - Kanban view with CPU-based status indicators.
  - Line graphs for CPU and RAM trends over time.
  - Pie charts for application CPU usage distribution.
- **Search Filters**: Filter metrics by time ranges (last 5 minutes, 1 hour, 3 hours, 24 hours, 7 days).
- **Security**: Configurable access controls for different user groups.

## Installation

### Prerequisites
- Odoo 17.0 installed and running.
- Python dependencies: `python-dateutil` (usually included with Odoo).
- Access to the Odoo server file system and database.

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/BotirBakhtiyarov/system_monitor.git
   ```

2. **Copy to Odoo Addons**:
   Move the `system_monitor` folder to your Odoo addons directory (e.g., `/path/to/odoo/custom_addons/`).

3. **Update Odoo Modules List**:
   Start or restart your Odoo server with the `--update` flag to register the module:
   ```bash
   ./odoo-bin -c /path/to/odoo.conf --update=system_monitor
   ```

4. **Install the Module**:
   - Log in to Odoo as an administrator.
   - Go to **Apps** > **Update Apps List**.
   - Search for "System Monitor" and click **Install**.

## Configuration

1. **API Endpoint**:
   - The module exposes a public API endpoint at `/api/data` for POST requests.
   - Configure your monitoring agent to send JSON payloads with the following structure:
     ```json
     {
       "computer_id": "unique_computer_id",
       "username": "user_name",
       "timestamp": "2025-05-07T12:00:00",
       "cpu": 45.5,
       "ram": {
         "total": 8589934592,
         "used": 4294967296,
         "percent": 50.0
       },
       "apps": {
         "app_name": {
           "duration": 3600,
           "cpu": 10.0,
           "ram": 104857600
         }
       }
     }
     ```

2. **Access Rights**:
   - By default, the module grants read, write, create, and unlink permissions to the `base.group_user` group.
   - Modify `security/ir.model.access.csv` to adjust permissions as needed.

## Usage

1. **Access the Module**:
   - After installation, navigate to the **System Monitor** menu in Odoo.
   - Sub-menus include:
     - **Computers**: View and manage monitored computers (kanban, tree, form views).
     - **Metrics**: Analyze system metrics (graph, tree, form, pivot views).

2. **Monitor Computers**:
   - The kanban view shows computer status (active/inactive) and latest CPU/RAM usage.
   - Colors indicate CPU usage: green (≤50%), yellow (>50%), red (>80%).

3. **Analyze Metrics**:
   - Use the graph view to visualize CPU and RAM trends (aggregated by day).
   - Apply time-based filters (e.g., "Last 24 Hours") in the search view.
   - The pivot view allows for detailed data analysis.

4. **Application Usage**:
   - View application-specific metrics in the metric form view or pie chart.

## Development

### Folder Structure
```
system_monitor/
├── controller/
│   ├── __init__.py
│   └── metrics_controller.py
├── models/
│   ├── __init__.py
│   └── system_metrics.py
├── security/
│   └── ir.model.access.csv
├── views/
│   ├── computer_views.xml
│   └── metrics_views.xml
├── __init__.py
├── __manifest__.py
└── README.md
```

### Extending the Module
- **Add New Metrics**: Extend the `system.monitor.metric` model in `models/system_metrics.py` to include additional fields (e.g., disk usage).
- **Custom Views**: Modify `views/computer_views.xml` or `views/metrics_views.xml` to add new view types or fields.
- **API Enhancements**: Update `controller/metrics_controller.py` to handle additional data types or validation rules.

### Running Tests
- Use Odoo's testing framework to write unit tests in a `tests/` directory.
- Example test command:
  ```bash
  ./odoo-bin -c /path/to/odoo.conf --test-enable --stop-after-init
  ```

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a Pull Request.

## License

This module is licensed under the [LGPL-3](https://www.gnu.org/licenses/lgpl-3.0.en.html). See the `__manifest__.py` for details.

## Support

For issues, feature requests, or questions, please open an issue on the [GitHub Issues page](https://github.com/botirbakhtiyarov/system_monitor/issues).

---

*Built with ❤️ for Odoo 17 by Botir Bakhtiyarov*
