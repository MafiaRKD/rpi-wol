#!/usr/bin/env bash

set -Eeuo pipefail

# ============================================================
# Homelab Dashboard Installer
# ============================================================

APP_NAME="Homelab Dashboard"
REPO_URL="https://github.com/MafiaRKD/rpi-wol.git"
SERVICE_NAME="wol-web.service"

# ------------------------------------------------------------
# Output helpers
# ------------------------------------------------------------

info() {
    echo
    echo "==> $1"
}

success() {
    echo
    echo "========================================"
    echo " $1"
    echo "========================================"
}

error() {
    echo
    echo "ERROR: $1" >&2
}

# ------------------------------------------------------------
# Basic checks
# ------------------------------------------------------------

if [[ "$(uname -s)" != "Linux" ]]; then
    error "This installer is intended for Linux systems."
    exit 1
fi

if [[ "${EUID}" -eq 0 ]]; then
    error "Do not run this installer as root."
    echo "Run it as your normal user. The installer will use sudo when required."
    exit 1
fi

INSTALL_USER="$(id -un)"
USER_HOME="${HOME}"
INSTALL_DIR="${USER_HOME}/rpi-wol"
CONFIG_FILE="${INSTALL_DIR}/config.json"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}"

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

require_sudo() {
    if ! command -v sudo >/dev/null 2>&1; then
        error "sudo is required but is not installed."
        exit 1
    fi

    info "Checking sudo access..."
    sudo -v
}

backup_config() {
    if [[ ! -f "${CONFIG_FILE}" ]]; then
        return 0
    fi

    local timestamp
    local backup_file

    timestamp="$(date '+%Y-%m-%d_%H-%M-%S')"
    backup_file="${USER_HOME}/config.json.backup.${timestamp}"

    cp "${CONFIG_FILE}" "${backup_file}"

    echo
    echo "Backup config created here:"
    echo "  ${backup_file}"
}

install_system_packages() {
    info "Installing required system packages..."

    sudo apt update

    sudo apt install -y \
        git \
        python3 \
        python3-venv \
        python3-pip \
        nut-client \
        curl
}

create_virtual_environment() {
    info "Creating Python virtual environment..."

    cd "${INSTALL_DIR}"

    rm -rf .venv

    python3 -m venv .venv

    "${INSTALL_DIR}/.venv/bin/pip" install --upgrade pip
    "${INSTALL_DIR}/.venv/bin/pip" install -r requirements.txt
}

create_config_if_missing() {
    if [[ ! -f "${CONFIG_FILE}" ]]; then
        info "Creating config.json..."
        cp "${INSTALL_DIR}/config.example.json" "${CONFIG_FILE}"
    else
        info "Existing config.json preserved."
    fi
}

install_systemd_service() {
    info "Installing systemd service..."

    if [[ ! -f "${INSTALL_DIR}/systemd/wol-web.service" ]]; then
        error "systemd service template was not found."
        exit 1
    fi

    sed "s/YOUR_USERNAME/${INSTALL_USER}/g" \
        "${INSTALL_DIR}/systemd/wol-web.service" \
        | sudo tee "${SERVICE_FILE}" >/dev/null

    sudo systemctl daemon-reload
    sudo systemctl enable "${SERVICE_NAME}"
}

start_service() {
    info "Starting ${APP_NAME}..."

    sudo systemctl restart "${SERVICE_NAME}"

    sleep 2

    if systemctl is-active --quiet "${SERVICE_NAME}"; then
        echo "Service status: active"
    else
        echo
        echo "WARNING: The service is not currently active."
        echo
        echo "Check the logs with:"
        echo "  journalctl -u ${SERVICE_NAME} -n 50"
    fi
}

get_ip_address() {
    hostname -I 2>/dev/null | awk '{print $1}'
}

show_configuration_notice() {
    echo
    echo "IMPORTANT - CONFIGURATION REQUIRED"
    echo "----------------------------------"
    echo
    echo "A default configuration file has been created."
    echo
    echo "Default login:"
    echo "  Username: admin"
    echo "  Password: change_me"
    echo
    echo "Edit the configuration:"
    echo "  nano ${CONFIG_FILE}"
    echo
    echo "Change at least:"
    echo "  - secret_key"
    echo "  - username"
    echo "  - password"
    echo "  - Wake-on-LAN broadcast address"
    echo "  - device names"
    echo "  - device MAC addresses"
    echo "  - device IP addresses"
    echo
    echo "After editing the configuration, restart the dashboard:"
    echo "  sudo systemctl restart ${SERVICE_NAME}"
    echo
}

show_install_summary() {
    local ip_address

    ip_address="$(get_ip_address)"

    success "${APP_NAME} installation complete"

    echo
    echo "Installation directory:"
    echo "  ${INSTALL_DIR}"

    echo
    echo "Configuration:"
    echo "  ${CONFIG_FILE}"

    echo
    echo "Service status:"
    echo "  systemctl status ${SERVICE_NAME}"

    echo
    echo "Service logs:"
    echo "  journalctl -u ${SERVICE_NAME} -f"

    if [[ -n "${ip_address}" ]]; then
        echo
        echo "Dashboard:"
        echo "  http://${ip_address}:5000"
    fi

    show_configuration_notice
}

show_update_summary() {
    local ip_address

    ip_address="$(get_ip_address)"

    success "${APP_NAME} update complete"

    echo
    echo "Configuration preserved:"
    echo "  ${CONFIG_FILE}"

    echo
    echo "Service status:"
    echo "  systemctl status ${SERVICE_NAME}"

    if [[ -n "${ip_address}" ]]; then
        echo
        echo "Dashboard:"
        echo "  http://${ip_address}:5000"
    fi

    echo
}

# ------------------------------------------------------------
# Installation actions
# ------------------------------------------------------------

fresh_install() {
    require_sudo

    install_system_packages

    info "Cloning ${APP_NAME}..."

    git clone "${REPO_URL}" "${INSTALL_DIR}"

    create_virtual_environment
    create_config_if_missing
    install_systemd_service
    start_service
    show_install_summary
}

update_installation() {
    require_sudo

    info "Updating ${APP_NAME}..."

    sudo systemctl stop "${SERVICE_NAME}" 2>/dev/null || true

    cd "${INSTALL_DIR}"

    if [[ ! -d ".git" ]]; then
        error "The existing installation is not a Git repository."
        echo "Use Reinstall instead."
        exit 1
    fi

    if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
        error "Local tracked files have been modified."
        echo "Update cancelled to prevent overwriting local changes."
        echo
        echo "Check:"
        echo "  cd ${INSTALL_DIR}"
        echo "  git status"
        exit 1
    fi

    git fetch origin
    git checkout main
    git pull --ff-only origin main

    info "Updating Python dependencies..."

    if [[ ! -x "${INSTALL_DIR}/.venv/bin/python" ]]; then
        info "Python virtual environment not found. Creating it..."
        python3 -m venv "${INSTALL_DIR}/.venv"
    fi

    "${INSTALL_DIR}/.venv/bin/pip" install --upgrade pip
    "${INSTALL_DIR}/.venv/bin/pip" install -r "${INSTALL_DIR}/requirements.txt"

    create_config_if_missing
    install_systemd_service
    start_service
    show_update_summary
}

reinstall_application() {
    require_sudo

    info "Preparing clean reinstall..."

    backup_config

    sudo systemctl stop "${SERVICE_NAME}" 2>/dev/null || true
    sudo systemctl disable "${SERVICE_NAME}" 2>/dev/null || true

    sudo rm -f "${SERVICE_FILE}"
    sudo systemctl daemon-reload

    info "Removing existing installation..."
    rm -rf "${INSTALL_DIR}"

    install_system_packages

    info "Cloning clean installation..."
    git clone "${REPO_URL}" "${INSTALL_DIR}"

    create_virtual_environment

    info "Creating fresh config.json..."
    cp "${INSTALL_DIR}/config.example.json" "${CONFIG_FILE}"

    install_systemd_service
    start_service
    show_install_summary
}

uninstall_application() {
    require_sudo

    echo
    echo "This will remove ${APP_NAME} from this system."
    echo "The current config.json will be backed up to your home directory."
    echo

    read -r -p "Continue with uninstall? [y/N]: " answer

    case "${answer}" in
        y|Y|yes|YES)
            ;;
        *)
            echo "Uninstall cancelled."
            exit 0
            ;;
    esac

    backup_config

    info "Stopping and removing systemd service..."

    sudo systemctl stop "${SERVICE_NAME}" 2>/dev/null || true
    sudo systemctl disable "${SERVICE_NAME}" 2>/dev/null || true

    sudo rm -f "${SERVICE_FILE}"

    sudo systemctl daemon-reload
    sudo systemctl reset-failed 2>/dev/null || true

    info "Removing application..."
    rm -rf "${INSTALL_DIR}"

    success "${APP_NAME} uninstalled"

    echo
    echo "The application and systemd service have been removed."
    echo "System packages were left installed."
    echo
    echo "Configuration backups are stored directly in:"
    echo "  ${USER_HOME}"
    echo
}

# ------------------------------------------------------------
# Existing installation menu
# ------------------------------------------------------------

existing_installation_menu() {
    echo
    echo "Existing installation detected:"
    echo "  ${INSTALL_DIR}"
    echo
    echo "1) Update"
    echo "2) Reinstall"
    echo "3) Uninstall"
    echo "4) Cancel"
    echo

    read -r -p "Select an option [1-4]: " choice

    case "${choice}" in
        1)
            update_installation
            ;;
        2)
            reinstall_application
            ;;
        3)
            uninstall_application
            ;;
        4)
            echo "Cancelled."
            exit 0
            ;;
        *)
            error "Invalid option."
            exit 1
            ;;
    esac
}

# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

echo
echo "========================================"
echo " ${APP_NAME} Installer"
echo "========================================"

if [[ -d "${INSTALL_DIR}" ]]; then
    existing_installation_menu
else
    fresh_install
fi