from flask import Flask, render_template, request, redirect, url_for, session
import subprocess
import platform

app = Flask(__name__)
app.secret_key = 'supersecretkey'

devices = {
    "Herný PC": {
        "mac": "DC:A6:32:BC:12:9F",
        "ip": "192.168.0.101"
    },
    "Server": {
        "mac": "00:11:22:33:44:55",
        "ip": "192.168.0.102"
    },
    "Notebook": {
        "mac": "66:77:88:99:AA:BB",
        "ip": "192.168.0.103"
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
        ip = info.get("ip")
        status_info[name] = {
            "mac": info["mac"],
            "online": is_online(ip) if ip else False
        }

    return render_template("index.html", devices=status_info)

@app.route("/wake/<device_name>")
def wake(device_name):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    device = devices.get(device_name)
    if device:
        subprocess.run(["wakeonlan", device["mac"]])
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
