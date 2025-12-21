from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
import platform

app = Flask(__name__)
app.secret_key = 'supersecretkey'

devices = {
    "Herný PC": {
        "mac": "AA:BB:CC:DD:EE:FF",
        "wol_ip": "192.168.0.100",
        "check_ip": "192.168.0.100"
    },
    "Server": {
        "mac": "AA:BB:CC:DD:EE:FF",
        "wol_ip": "192.168.0.101",
        "check_ip": "192.168.0.101"
    },
    "ProxMox": {
        "mac": "AA:BB:CC:DD:EE:FF",
        "wol_ip": "192.168.0.100",
        "check_ip": "192.168.0.103"
    },
    "Xubuntu": {
        "mac": "AA:BB:CC:DD:EE:FF",
        "wol_ip": "192.168.0.100",      # WoL posielame na ProxMox
        "check_ip": "192.168.0.250"   # skutočná IP VM-ky
    }
}

USERNAME = "admin"
PASSWORD = "tajneheslo"

def is_online(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        result = subprocess.run(["ping", param, "1", ip], stdout=subprocess.DEVNULL)
        return result.returncode == 0
    except:
        return False

def get_cpu_temp():
    try:
        output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
        if "temp=" in output:
            temp = output.strip().replace("temp=", "")
            print("Teplota CPU:", temp)
            return temp
    except Exception as e:
        print("Chyba pri čítaní teploty:", e)
    return "Neznáma"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("index"))
        return render_template("login.html", error="Zlé meno alebo heslo.")
    return render_template("login.html")

@app.route("/home")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    status_info = {}
    for name, info in devices.items():
        check_ip = info.get("check_ip")
        wol_ip = info.get("wol_ip")  # zatiaľ nepoužívame, ale máme ho pripravený

        # Kontrola online stavu podľa check_ip
        online = is_online(check_ip) if check_ip else False

        status_info[name] = {
            "mac": info["mac"],
            "online": online,
            "wol_ip": wol_ip  # ak by si chcel neskôr niečo špeciálne
        }

    cpu_temp = get_cpu_temp()
    print("cpu_temp premenná:", cpu_temp)  # debug print
    return render_template("index.html", devices=status_info, cpu_temp=cpu_temp)

@app.route("/wake/<device_name>")
def wake(device_name):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    device = devices.get(device_name)
    if device and "wol_ip" in device:
        # Wake-on-LAN posielame na správnu IP (väčšinou broadcast, ale wakeonlan to zvládne)
        subprocess.run(["wakeonlan", "-i", device["wol_ip"], device["mac"]])
        # Poznámka: -i parameter nie je povinný, wakeonlan defaultne posiela na broadcast,
        # ale ak máš problémy, môžeš špecifikovať -i 192.168.0.255 alebo podobné
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
