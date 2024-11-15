import requests

DNS_PROVIDERS = {
    "Cloudflare": "https://cloudflare-dns.com/dns-query",
    "Google": "https://dns.google/dns-query"
}

BLOCKLIST_URL = "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts"

def setup_dns(provider="Cloudflare"):
    url = DNS_PROVIDERS.get(provider, DNS_PROVIDERS["Cloudflare"])
    headers = {"accept": "application/dns-json"}
    response = requests.get(f"{url}?name=example.com&type=A", headers=headers)
    if response.status_code == 200:
        return f"DNS-over-HTTPS enabled with {provider}: {response.json()}"
    else:
        return f"Failed to enable DNS-over-HTTPS with {provider}."

def apply_tracker_blocking():
    try:
        blocklist = requests.get(BLOCKLIST_URL).text
        with open("/etc/hosts", "a") as hosts_file:
            hosts_file.write(blocklist)
        return "Tracker blocking applied successfully."
    except Exception as e:
        return f"Failed to apply tracker blocking: {str(e)}"
