# Changelog

## 2.0.0

### Added

- Modular service architecture
- REST API endpoints
- Live dashboard updates
- AJAX Wake-on-LAN
- Automatic online/offline device monitoring
- CPU temperature monitoring
- NUT UPS monitoring
- UPS battery charge, runtime and load information
- Dark responsive interface
- Authentication
- External configuration file
- Python virtual environment support
- systemd service for automatic startup
- Automatic startup after system reboot
- Project documentation
- Installation and update instructions

### Changed

- Project reorganized into modules
- CSS moved to a dedicated stylesheet
- JavaScript separated from templates
- Configuration handling moved to `config.py`
- Wake-on-LAN actions no longer require a page reload
- Device status is refreshed automatically
- Wake buttons reflect the current device state
- UPS dashboard card simplified to essential information
- Application service now runs inside a Python virtual environment

### Removed

- Full page reload after Wake-on-LAN requests
- Unnecessary UPS input and output voltage values