# Wake-on-LAN Web Interface pre Raspberry Pi

Jednoduché a bezpečné webové rozhranie pre zapínanie viacerých počítačov cez Wake-on-LAN (WOL) pomocou Raspberry Pi.

## 🔧 Funkcie

- 🖥 Zapínanie viacerých PC v sieti (MAC adresy)
- 🔐 Ochrana heslom
- 🔁 Automatické spustenie ako systemd služba
- 💡 Funguje na Raspberry Pi 2, 3, 4 (alebo inom Linuxe)

## 🛠️ Inštalácia

### 1. Závislosti

```bash
sudo apt update
sudo apt install wakeonlan python3-flask unzip git -y
```

### 2. Stiahnutie a spustenie

```bash
cd ~
git clone https://github.com/MafiaRKD/rpi-wol.git
cd rpi-wol
```

> 📝 Uprav súbor `app.py` – zmeň:
> - MAC adresy zariadení v `devices = {...}`
> - prihlasovacie údaje (`USERNAME`, `PASSWORD`)

### 3. Spustenie služby

```bash
sudo cp wol-web.service /etc/systemd/system/
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable wol-web
sudo systemctl start wol-web
```

### 4. Použitie

Otvor prehliadač:

```
http://<IP_Raspberry_Pi>:5000
```

## 🔐 Prihlásenie

- Meno: `admin`
- Heslo: `tajneheslo` *(zmeň v `app.py` pred použitím!)*

## 📂 Štruktúra projektu

```
rpi-wol/
├── app.py
├── wol-web.service
└── templates/
    ├── index.html
    └── login.html
```

## 🔒 Odporúčania

- Zabezpečiť prístup cez firewall alebo VPN
- Voliteľne: pridať HTTPS (napr. cez Nginx + certbot)
