# Homelab Dashboard

A lightweight Flask dashboard for Raspberry Pi and other Linux systems.

Originally created as a simple Wake-on-LAN utility, the project has evolved into a modular dashboard for monitoring and managing homelab devices.

> **Current version:** 2.0.0

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
- Optimized for Raspberry Pi

---

## Screenshot

![Homelab Dashboard](docs/screenshot.png)

---

## Requirements

Recommended platform:

- Raspberry Pi
- Raspberry Pi OS / Debian-based Linux
- Python 3.10 or newer
- Git
- Python virtual environment support

Optional:

- Network UPS Tools (NUT) client for UPS monitoring

Python dependencies such as Flask and wakeonlan are installed from `requirements.txt`.

---

## Installation

### 1. Install system dependencies

Update the package list:

```bash
sudo apt update
```

Install Git, Python virtual environment support and pip:

```bash
sudo apt install git python3-venv python3-pip -y
```

If you want to use UPS monitoring, also install the NUT client:

```bash
sudo apt install nut-client -y
```

---

### 2. Clone the repository

```bash
cd ~
git clone https://github.com/MafiaRKD/rpi-wol.git
cd rpi-wol
```

---

### 3. Create a Python virtual environment

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create your local configuration from the included example:

```bash
cp config.example.json config.json
```

Edit it:

```bash
nano config.json
```

Configure your:

- application title
- secret key
- login credentials
- Wake-on-LAN broadcast address
- monitored devices
- UPS connection

`config.json` is excluded from Git and will not be committed to the repository.

### Device configuration

Each monitored device requires an ID, display name, MAC address and IP address.

Example:

```json
{
  "id": "server",
  "name": "Server",
  "mac": "AA:BB:CC:DD:EE:FF",
  "check_ip": "192.168.0.10"
}
```

The MAC address is used for Wake-on-LAN and `check_ip` is used for online/offline monitoring.

---

## UPS Monitoring

UPS monitoring is optional and uses Network UPS Tools (NUT).

The dashboard can display:

- UPS status
- battery charge
- estimated runtime
- UPS load

The NUT server may run on another device, such as TrueNAS.

Before enabling UPS monitoring in the dashboard, verify that the Raspberry Pi can communicate with your NUT server.

Example:

```bash
upsc ups@192.168.0.2
```

A shorter diagnostic command can be used to display the values required by the dashboard:

```bash
upsc ups@192.168.0.2 | grep -E "ups.status|battery.charge|battery.runtime|ups.load"
```

Then configure the UPS section in `config.json` with the correct NUT server address and UPS name.

If UPS monitoring is disabled or the NUT client is unavailable, the rest of the dashboard continues to operate normally.

---

## Running as a systemd Service

A systemd service template is included in:

```text
systemd/wol-web.service
```

Before installing it, edit the service file:

```bash
nano systemd/wol-web.service
```

Replace every occurrence of:

```text
YOUR_USERNAME
```

with your Linux username.

You can check your username with:

```bash
whoami
```

For example, if the username is `pi`, the relevant part of the service should look like:

```ini
[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/rpi-wol
ExecStart=/home/pi/rpi-wol/.venv/bin/python /home/pi/rpi-wol/app.py

Environment=PYTHONUNBUFFERED=1

Restart=always
RestartSec=5
```

Install the service:

```bash
sudo cp systemd/wol-web.service /etc/systemd/system/wol-web.service
```

Reload systemd:

```bash
sudo systemctl daemon-reload
```

Enable automatic startup:

```bash
sudo systemctl enable wol-web.service
```

Start the dashboard:

```bash
sudo systemctl start wol-web.service
```

Check its status:

```bash
systemctl status wol-web.service
```

The service should report:

```text
Active: active (running)
```

Open the dashboard in your browser:

```text
http://<raspberry-pi-ip>:5000
```

The dashboard will now start automatically whenever the Raspberry Pi boots.

---

## Service Management

Restart the dashboard:

```bash
sudo systemctl restart wol-web.service
```

Stop the dashboard:

```bash
sudo systemctl stop wol-web.service
```

Start the dashboard:

```bash
sudo systemctl start wol-web.service
```

Check the service status:

```bash
systemctl status wol-web.service
```

---

## Logs

View the service logs:

```bash
journalctl -u wol-web.service
```

Follow the logs live:

```bash
journalctl -u wol-web.service -f
```

Show logs from the current boot:

```bash
journalctl -u wol-web.service -b
```

---

## Updating

Go to the application directory:

```bash
cd ~/rpi-wol
```

Pull the latest version:

```bash
git pull
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install or update Python dependencies:

```bash
pip install -r requirements.txt
```

Restart the service:

```bash
sudo systemctl restart wol-web.service
```

Verify that the service started correctly:

```bash
systemctl status wol-web.service
```

Your local `config.json` is ignored by Git and is preserved during normal updates.

---

## Project Structure

```text
rpi-wol/
├── api/
├── docs/
├── services/
├── static/
│   ├── css/
│   └── js/
├── systemd/
├── templates/
├── app.py
├── config.py
├── config.example.json
├── requirements.txt
├── CHANGELOG.md
├── LICENSE
└── README.md
```

### Main components

- `app.py` — Flask application and routes
- `api/` — dashboard API endpoints
- `services/` — Wake-on-LAN, network, UPS and system services
- `static/` — CSS and JavaScript
- `templates/` — HTML templates
- `config.py` — configuration loader
- `config.json` — local configuration, not tracked by Git
- `config.example.json` — example configuration
- `systemd/` — systemd service template

---

## Tested Platform

Version 2.0.0 has been tested on a Raspberry Pi running Python 3.11 with:

- automatic systemd startup
- Python virtual environment
- Wake-on-LAN
- automatic device status monitoring
- CPU temperature monitoring
- remote NUT UPS monitoring
- automatic startup after Raspberry Pi reboot

---

## Security

The dashboard is intended primarily for trusted home networks.

Do not expose the Flask development server directly to the public Internet.

If remote access is required, use an appropriate secure reverse proxy, VPN or other protected access method.

Keep `config.json` private because it contains local configuration and authentication credentials.

---

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.