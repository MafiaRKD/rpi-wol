# Changelog

## 2.0.1

### Added

- Automatic one-line installer
- Existing installation detection
- Installer Update mode
- Installer Reinstall mode
- Installer Uninstall mode
- Automatic configuration backup before Reinstall
- Automatic configuration backup before Uninstall
- Automatic system package installation
- Automatic Python virtual environment creation
- Automatic systemd service configuration
- Application version management through `version.py`
- Homelab Dashboard logo
- Browser favicon
- Static asset cache busting based on application version

### Changed

- Application version is no longer stored in `config.json`
- Updates now preserve user configuration independently of the application version
- Installation process is fully automated
- systemd service is automatically configured for the current Linux user
- README installation and update instructions updated for the automatic installer
- Dashboard and login page updated with Homelab Dashboard branding

### Fixed

- Prevented stale CSS and JavaScript files from being used after application updates
- Fixed application version remaining outdated when preserving `config.json` during updates

---

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