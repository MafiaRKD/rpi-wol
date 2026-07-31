# Homelab Dashboard

A lightweight Flask dashboard for Raspberry Pi and other Debian-based Linux systems.

Originally created as a simple Wake-on-LAN utility, the project has evolved into a modular dashboard for monitoring and managing homelab devices.

> **Current version:** 2.0.1

---

## Features

- Wake-on-LAN for multiple devices
- Live online/offline status monitoring
- Automatic dashboard refresh
- CPU temperature monitoring
- NUT UPS monitoring
- Modern dark user interface
- AJAX-based Wake-on-LAN controls
- Simple authentication
- Modular service architecture
- Lightweight Flask backend
- systemd support for automatic startup
- Automatic installer, updater and uninstaller
- Optimized for Raspberry Pi

---

## Screenshot

![Homelab Dashboard](docs/screenshot.png)

---

## Quick Installation

The recommended installation method is the automatic installer.

Run the following command as your normal Linux user:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/MafiaRKD/rpi-wol/main/install.sh)"
```

Do not run the installer with `sudo`. It will request sudo privileges automatically when required.

The installer automatically:

- installs required system packages
- clones the repository to `~/rpi-wol`
- creates a Python virtual environment
- installs Python dependencies
- creates `config.json`
- configures the systemd service for the current user
- enables automatic startup
- starts the dashboard

After installation, open:

```text
http://<raspberry-pi-ip>:5000
```

Default login:

```text
Username: admin
Password: change_me
```

Edit the configuration after installation:

```bash
nano ~/rpi-wol/config.json
```

At minimum, change:

- secret key
- username
- password
- Wake-on-LAN broadcast address
- device names
- device MAC addresses
- device IP addresses

Then restart the dashboard:

```bash
sudo systemctl restart wol-web.service
```

---

## Installer Management

Running the installer again detects the existing installation:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/MafiaRKD/rpi-wol/main/install.sh)"
```

The following menu is displayed:

```text
Existing installation detected:
  /home/<user>/rpi-wol

1) Update
2) Reinstall
3) Uninstall
4) Cancel
```

### Update

Updates the application to the latest version while preserving the existing:

```text
config.json
```

The installer also updates Python dependencies, refreshes the systemd service and restarts the dashboard.

If tracked application files contain local modifications, the update is cancelled to prevent accidentally overwriting them.

### Reinstall

Performs a clean application reinstall.

Before removing the existing installation, the current configuration is backed up to:

```text
~/config.json.backup.YYYY-MM-DD_HH-MM-SS
```

The application is then installed again with a fresh default `config.json`.

The backup is not restored automatically.

### Uninstall

Stops and removes:

- Homelab Dashboard
- `~/rpi-wol`
- `wol-web.service`

Before removal, the current configuration is backed up to:

```text
~/config.json.backup.YYYY-MM-DD_HH-MM-SS
```

System packages installed by the installer are intentionally left installed.

---

## Requirements

Recommended platform:

- Raspberry Pi
- Raspberry Pi OS / Debian-based Linux
- Internet connection
- `curl`
- normal user account with sudo access

The automatic installer handles the remaining dependencies, including:

- Git
- Python 3
- Python virtual environment support
- pip
- Network UPS Tools client

---

## Configuration

The local configuration is stored in:

```text
~/rpi-wol/config.json
```

The file is created automatically during installation from:

```text
config.example.json
```

`config.json` is excluded from Git and is preserved during normal updates.

### Device configuration

Each monitored device requires:

- ID
- display name
- MAC address
- IP address

Example:

```json
{
  "id": "server",
  "name": "Server",
  "mac": "AA:BB:CC:DD:EE:FF",
  "check_ip": "192.168.0.10"
}
```

The MAC address is used for Wake-on-LAN.

`check_ip` is used for automatic online/offline monitoring.

---

## UPS Monitoring

UPS monitoring is optional and uses Network UPS Tools (NUT).

The dashboard can display:

- UPS status
- battery charge
- estimated runtime
- UPS load

The NUT server may run on another device, such as TrueNAS.

Before enabling UPS monitoring, verify that the Raspberry Pi can communicate with the NUT server.

Example:

```bash
upsc ups@192.168.0.2
```

A shorter diagnostic command can display the values used by the dashboard:

```bash
upsc ups@192.168.0.2 | grep -E "ups.status|battery.charge|battery.runtime|ups.load"
```

Then configure the UPS section in:

```text
~/rpi-wol/config.json
```

If UPS monitoring is disabled or the NUT server is unavailable, the rest of the dashboard continues to operate normally.

---

## Service Management

The installer creates:

```text
/etc/systemd/system/wol-web.service
```

The service starts automatically when the system boots.

Check status:

```bash
systemctl status wol-web.service
```

Restart:

```bash
sudo systemctl restart wol-web.service
```

Stop:

```bash
sudo systemctl stop wol-web.service
```

Start:

```bash
sudo systemctl start wol-web.service
```

---

## Logs

View service logs:

```bash
journalctl -u wol-web.service
```

Follow logs live:

```bash
journalctl -u wol-web.service -f
```

Show logs from the current boot:

```bash
journalctl -u wol-web.service -b
```

---

## Manual Installation

The automatic installer is recommended.

For manual installation, install the required packages:

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip nut-client
```

Clone the repository:

```bash
cd ~
git clone https://github.com/MafiaRKD/rpi-wol.git
cd rpi-wol
```

Create the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Create the configuration:

```bash
cp config.example.json config.json
nano config.json
```

The systemd template is located at:

```text
systemd/wol-web.service
```

Replace every occurrence of:

```text
YOUR_USERNAME
```

with your Linux username.

Install and enable the service:

```bash
sudo cp systemd/wol-web.service /etc/systemd/system/wol-web.service
sudo systemctl daemon-reload
sudo systemctl enable wol-web.service
sudo systemctl start wol-web.service
```

Verify:

```bash
systemctl status wol-web.service
```

The dashboard should now be available at:

```text
http://<raspberry-pi-ip>:5000
```

---

## Project Structure

```text
rpi-wol/
├── api/
├── docs/
├── services/
├── static/
│   ├── css/
│   ├── js/
│   ├── favicon.ico
│   └── homelab-dashboard-logo.png
├── systemd/
├── templates/
├── app.py
├── config.py
├── config.example.json
├── install.sh
├── requirements.txt
├── version.py
├── CHANGELOG.md
├── LICENSE
└── README.md
```

### Main components

- `app.py` — Flask application and routes
- `api/` — dashboard API endpoints
- `services/` — Wake-on-LAN, network, UPS and system services
- `static/` — CSS, JavaScript and branding assets
- `templates/` — HTML templates
- `config.py` — configuration loader
- `config.json` — local configuration, not tracked by Git
- `config.example.json` — example configuration
- `version.py` — application version
- `install.sh` — automatic installer and management script
- `systemd/` — systemd service template

---

## Tested Platform

Version 2.0.1 has been tested on Raspberry Pi OS / Debian with Python 3.11.

The following installation and application functions have been tested:

- fresh installation using the one-line installer
- automatic installation of required system packages
- Python virtual environment creation
- automatic systemd service installation
- automatic startup after Raspberry Pi reboot
- installer Update
- configuration preservation during Update
- installer Reinstall
- configuration backup during Reinstall
- installer Uninstall
- configuration backup during Uninstall
- Wake-on-LAN
- automatic device status monitoring
- CPU temperature monitoring
- remote NUT UPS monitoring

---

## Security

The dashboard is intended primarily for trusted home networks.

The default credentials are:

```text
Username: admin
Password: change_me
```

**Change the default username, password and secret key after installation.**

Do not expose the Flask development server directly to the public Internet.

If remote access is required, use an appropriate secure reverse proxy, VPN or other protected access method.

Keep `config.json` and its backups private because they contain local configuration and authentication credentials.

---

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.