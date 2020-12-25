#!/usr/bin/env python3

import subprocess
import argparse
import re
from art import *

print("\33[33m")
tprint("MAC-CHANGER", "rand")
print("\33[39m")

def get_info():

	parser = argparse.ArgumentParser(description=" Easy To Use MAC-Changer \n")

	parser.add_argument("-i", "--interface", dest = "interface", help = "Name of the interface")
	parser.add_argument("-m", "--mac", dest = "new_mac", help = "Enter the MAC-Address")

	args = parser.parse_args()

	if not args.interface:
		parser.error("\n[-] Interface Missing!")

	elif not args.new_mac:
		parser.error("\n[-] New MAC-Address Missing!")
	
	return args

def get_mac(interface):
	result = str(subprocess.check_output(["ifconfig", interface]))
	macadd = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", result)

	if macadd:
		return macadd[0]
	else:
		print("\n[-] Could not find MAC Address")

def main():
	
	args = get_info()
	nmac = args.new_mac
	inter = args.interface
	vmac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", nmac)
	
	current_mac = get_mac(inter)
	print("\n[+] Current MAC Address: " + str(current_mac))

	if len(nmac) != 17:
		print("[-] Enter a valid MAC Address!")
	
	elif str(current_mac) == "None":
		exit()
	
	elif not vmac:
		print("[-] Enter a valid MAC Address!")

	else:
		print("[+] Changing MAC Address for " + inter + " to " + nmac)
		subprocess.call(["ifconfig" , inter , "down"])
		subprocess.call(["ifconfig" , inter , "hw", "ether", nmac])
		subprocess.call(["ifconfig" , inter , "up"])
	
		current_mac = get_mac(inter)

		if current_mac == nmac:
			print("\n[*] MAC Address is successfully changed to " + current_mac)
		else:
			print("[-] MAC Address could not change!!")

if __name__ == '__main__':
	main()
