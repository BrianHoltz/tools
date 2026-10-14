#!/bin/bash
# phantom-doctor: Off-VPN network/proxy diagnostics
#
# Run this manually while VPN is disconnected — an agent cannot run it then,
# since agent connectivity itself depends on the host network at that point.
#
# Checks connectivity, DNS resolution, proxy configuration, and known
# problem hosts (package registries, plugin marketplaces, etc.), then prints
# a plain report you can paste back to an agent once VPN is reconnected.
#
# Extend the HOSTS list below as new network failure modes are diagnosed.

echo "=== phantom-doctor: network diagnostics ==="
echo "Run date: $(date '+%Y-%m-%d %H:%M %Z')"
echo ""

echo "--- Basic connectivity ---"
if ping -c 1 -t 3 8.8.8.8 >/dev/null 2>&1; then
    echo "✓ Internet reachable (8.8.8.8)"
else
    echo "✗ No internet route to 8.8.8.8 — check Wi-Fi/Ethernet"
fi
echo ""

echo "--- Proxy environment ---"
for var in HTTP_PROXY HTTPS_PROXY NO_PROXY http_proxy https_proxy no_proxy; do
    val="${!var}"
    if [ -n "$val" ]; then
        echo "$var=$val"
    fi
done
if [ -z "$HTTP_PROXY$HTTPS_PROXY$http_proxy$https_proxy" ]; then
    echo "(no proxy env vars set)"
fi
echo ""

echo "--- macOS system proxy (networksetup) ---"
service=$(networksetup -listallnetworkservices 2>/dev/null | grep -v '^\*' | grep -iE 'wi-fi|ethernet' | head -1)
if [ -n "$service" ]; then
    echo "Service: $service"
    networksetup -getwebproxy "$service" 2>/dev/null
    networksetup -getsecurewebproxy "$service" 2>/dev/null
else
    echo "(could not detect active network service)"
fi
echo ""

echo "--- DNS resolution: known hosts ---"
HOSTS=(
    "8.8.8.8"
    "github.com"
    "registry.npmjs.org"
    "services.gradle.org"
    "plugins.jetbrains.com"
    "downloads.marketplace.jetbrains.com"
    "gecgithub01.walmart.com"
    "proxy-intlho.wal-mart.com"
)
for host in "${HOSTS[@]}"; do
    if [[ "$host" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        continue
    fi
    if result=$(dscacheutil -q host -a name "$host" 2>/dev/null | grep ip_address | head -1); then
        if [ -n "$result" ]; then
            echo "✓ $host → ${result#ip_address: }"
        else
            echo "✗ $host — DNS lookup failed"
        fi
    fi
done
echo ""

echo "--- VPN state heuristic ---"
if ifconfig | grep -qE "^utun[0-9]+:" && scutil --nwi 2>/dev/null | grep -q "Network interfaces: .*utun"; then
    echo "VPN-looking interface present (utun). May still be disconnected from Zscaler service."
else
    echo "No active VPN-looking interface detected — likely off-VPN."
fi
echo ""

echo "=== End phantom-doctor report ==="
echo "Paste this output back to your agent when VPN is reconnected."
