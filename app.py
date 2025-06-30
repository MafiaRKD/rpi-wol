from flask import Flask, render_template, request, redirect, url_for, session
import subprocess

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Zmeň si tento kľúč

# MAC adresy zariadení (pridať ľubovoľné)
devices = {
    "Herný PC": "DC:A6:32:BC:12:9F",
    "Server": "00:11:22:33:44:55",
    "Notebook": "66:77:88:99:AA:BB"
}

# Jednoduché prihlasovanie
USERNAME = "admin"
PASSWORD = "tajneheslo"  # Zmeň si podľa seba

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
    return render_template("index.html", devices=devices)

@app.route("/wake/<device_name>")
def wake(device_name):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    mac = devices.get(device_name)
    if mac:
        subprocess.run(["wakeonlan", mac])
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
