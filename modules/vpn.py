import subprocess
import platform

VPN_PROVIDERS = {
    "NordVPN": "vpn_configs/nordvpn_config.ovpn",
    "ExpressVPN": "vpn_configs/expressvpn_config.ovpn",
    "Surfshark": "vpn_configs/surfshark_config.ovpn",
    "CyberGhost": "vpn_configs/cyberghost_config.ovpn",
    "PIA": "vpn_configs/pia_config.ovpn",
    "ProtonVPN": "vpn_configs/protonvpn_config.ovpn",
    "IPVanish": "vpn_configs/ipvanish_config.ovpn",
    "Mullvad": "vpn_configs/mullvad_config.ovpn",
    "Windscribe": "vpn_configs/windscribe_config.ovpn",
    "TunnelBear": "vpn_configs/tunnelbear_config.ovpn"
}

def connect_vpn(provider):
    os_type = platform.system()
    config_path = VPN_PROVIDERS.get(provider)
    if not config_path:
        return f"VPN configuration for {provider} not found."

    try:
        if os_type == "Linux" or os_type == "Darwin":  # macOS/Linux
            subprocess.run(["sudo", "openvpn", "--config", config_path], check=True)
        elif os_type == "Windows":
            subprocess.run(["openvpn.exe", "--config", config_path], check=True)
        else:
            return "Unsupported OS."
        return f"{provider} connected successfully."
    except subprocess.CalledProcessError:
        return f"Failed to connect to {provider}. Check your configuration."

def disconnect_vpn():
    os_type = platform.system()
    try:
        if os_type == "Linux" or os_type == "Darwin":
            subprocess.run(["sudo", "killall", "openvpn"], check=True)
        elif os_type == "Windows":
            subprocess.run(["taskkill", "/IM", "openvpn.exe", "/F"], check=True)
        else:
            return "Unsupported OS."
        return "VPN disconnected successfully."
    except subprocess.CalledProcessError:
        return "Failed to disconnect VPN."
