from wakeonlan import send_magic_packet


def wake(mac_address, broadcast):
    send_magic_packet(
        mac_address,
        ip_address=broadcast,
    )