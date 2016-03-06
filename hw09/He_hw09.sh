# Guanshi He
# ECE 404
# HW 09
# Firewall

# flush all of the rules in all of the tables
# -X option is for deleting chains
iptables -t filter -F
iptables -t filter -X

#place no restriction on outbound packets
iptables -A OUTPUT -j ACCEPT

#block a list of specific ip address for all incoming connections
iptables -A INPUT -s 10.10.10.0/255.255.255.0 -j DROP

#block your computer from being pinged by all other hosts
iptables -A INPUT -p icmp --icmp-type echo-request -j DROP

#set up port-forwarding from an unused port of your choice to port 22 on your computer
iptables -t nat -A PREROUTING -p tcp 192.168.0.1:123 --dport 22 -j DNAT --to-destination 192.168.0.1

#all for SSH access port 22 to your machine from only the ecn.purdue.edu domain
iptables -A INPUT -s 128.46.4.83 -p tcp --destination-port 22 -j ACCEPT

#allow only a single IP address in the internet to access your machine for the HTTP service
iptables -A INPUT -s 192.168.0.1 -p tcp --destination-port 80 -j ACCEPT

#permit auth/ident (port 113) that is used by some services like SMTP and IRC
iptables -A INPUT -p udp --destination-port 113 -j ACCEPT
iptables -A INPUT -p tcp --destination-port 113 -j ACCEPT

