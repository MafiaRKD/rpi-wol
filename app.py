from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from config import CONFIG
from version import APP_VERSION
from services.wol import wake
from services.network import is_online
from services.system import get_cpu_temp
from api.status import get_status

app = Flask(__name__)
app.secret_key = CONFIG["app"]["secret_key"]

DEVICES = CONFIG["devices"]


def get_device(device_id):
    for device in DEVICES:
        if device["id"] == device_id:
            return device

    return None


def get_devices_status():
    devices = []

    for device in DEVICES:
        devices.append(
            {
                "id": device["id"],
                "name": device["name"],
                "online": is_online(device["check_ip"]),
            }
        )

    return devices


@app.route("/", methods=["GET", "POST"])
def login():
    if session.get("logged_in"):
        return redirect(url_for("index"))

    error = None

    if request.method == "POST":
        if (
            request.form["username"] == CONFIG["auth"]["username"]
            and request.form["password"] == CONFIG["auth"]["password"]
        ):
            session["logged_in"] = True
            return redirect(url_for("index"))

        error = "Nesprávne používateľské meno alebo heslo."

    return render_template(
        "login.html",
        error=error,
        app_title=CONFIG["app"]["title"],
        app_version=APP_VERSION,
    )


@app.route("/home")
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template(
        "index.html",
        app_title=CONFIG["app"]["title"],
        app_version=APP_VERSION,
        devices=get_devices_status(),
        cpu_temp=get_cpu_temp(),
    )


@app.route("/api/status")
def api_status():
    if not session.get("logged_in"):
        return "", 401

    return get_status()


# -------- NOVÝ AJAX endpoint --------

@app.route("/api/wake/<device_id>", methods=["POST"])
def api_wake(device_id):
    if not session.get("logged_in"):
        return jsonify({"success": False}), 401

    device = get_device(device_id)

    if device is None:
        return jsonify({"success": False}), 404

    wake(
        device["mac"],
        CONFIG["wake_on_lan"]["broadcast"],
    )

    return jsonify({"success": True})


# -------- Starý endpoint ponechávame --------

@app.route("/wake/<device_id>")
def wake_device(device_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    device = get_device(device_id)

    if device:
        wake(
            device["mac"],
            CONFIG["wake_on_lan"]["broadcast"],
        )

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
    )