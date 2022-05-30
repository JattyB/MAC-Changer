#!/usr/bin/env python3

import subprocess
import argparse
import re
from art import *

author="------> Created By: JattyB"
strin1 = "|"
print("\33[33m")
tprint("MAC-CHANGER", "rand")
print(f"{strin1 : >75}")
print(f"{author : >100}")
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
	result = str(subprocess.check_output(["ip","addr","show", interface]))
	macadd = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", result)

	if macadd:
		return macadd[0]
	else:
		print("\n[-] Could not find MAC Address for the give interface")

def main():
	
	args = get_info()
	nmac = args.new_mac
	inter = args.interface
	vmac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", nmac)
	
	current_mac = get_mac(inter)
	with open("/tmp/last_mac.txt",'w') as f:
		f.write(current_mac)
	print("\n[+] Current MAC Address: " + str(current_mac))

	if len(nmac) != 17:
		print("[-] Enter a valid MAC Address!")
	
	elif str(current_mac) == "None":
		exit()
	
	elif not vmac:
		print("[-] Enter a valid MAC Address!")

	elif current_mac == nmac:
		print("[-] MAC Address already in use")

	else:
		print("[+] Changing MAC Address for " + inter + " to " + nmac)
		subprocess.call(["ip","link","set","dev" , inter , "down"])
		subprocess.call(["ip","link","set","dev" , inter , "address", nmac])
		subprocess.call(["ip","link","set","dev" , inter , "up"])
	
		current_mac = get_mac(inter)

		if current_mac == nmac:
			print("\n[*] MAC Address is successfully changed to " + current_mac)
		else:
			print("[-] MAC Address could not change!!")

if __name__ == '__main__':
	main()
