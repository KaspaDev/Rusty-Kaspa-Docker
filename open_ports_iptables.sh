# Allow inbound TCP on 16111 and 18110
sudo iptables -A INPUT -p tcp --dport 16111 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 18110 -j ACCEPT
# Save rules to persist (depends on your distro)
sudo iptables-save > /etc/iptables/rules.v4  # For Debian/Ubuntu
# Or, for CentOS/RHEL:
# sudo service iptables save
# Verify rules
sudo iptables -L -v -n --line-numbers | grep -E '16111|18110'
