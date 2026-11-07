#!/bin/bash
set -e

# Последние проверенные IP-адреса:
# Proxy:      192.168.0.100
# Backend:    192.168.0.199
# PostgreSQL: 192.168.0.165
# Redis:      192.168.0.138

if [ "$EUID" -ne 0 ]; then
    echo "Запусти сценарий через sudo."
    exit 1
fi

case "$1" in
    backend)
        ufw allow 22/tcp
        ufw allow from 192.168.0.100 to any port 8080 proto tcp
        ufw allow out to 192.168.0.165 port 5432 proto tcp
        ufw default deny incoming
        ufw default deny outgoing
        ufw --force enable
        ufw status verbose
        ;;

    postgres)
        ufw allow 22/tcp
        ufw allow from 192.168.0.199 to any port 5432 proto tcp
        ufw default deny incoming
        ufw default allow outgoing
        ufw --force enable
        ufw status verbose
        ;;

    redis)
        ufw allow 22/tcp
        ufw allow from 192.168.0.100 to any port 6379 proto tcp
        ufw default deny incoming
        ufw default allow outgoing
        ufw --force enable
        ufw status verbose
        ;;

    proxy)
        systemctl enable --now firewalld

        firewall-cmd --zone=public --add-service=ssh
        firewall-cmd --zone=public --add-port=5000/tcp

        firewall-cmd --permanent --zone=public --add-service=ssh
        firewall-cmd --permanent --zone=public --add-port=5000/tcp

        firewall-cmd --zone=public --list-all
        ;;

    *)
        echo "Использование: sudo bash rules.sh {backend|postgres|redis|proxy}"
        exit 1
        ;;
esac
