from tkinter import *
from tkinter import ttk
import random
import os
import re
import socket
import sys
import netmiko
import time
from getpass import getpass
from ciscoconfparse import CiscoConfParse

def to_doc(file_name, varable):
	f=open(file_name, 'w')
	f.write(varable)
	f.close()
	
def nexus_fix(file_name):
	print ("Nexus Fix")
	with open(file_name, 'r') as myfile:
		data=myfile.read().replace("admin state is","    admin state is")
	to_doc(file_name,data)

def find_all_numbers(line):
	tmp = [int(s) for s in line.split() if s.isdigit()]
	total = 0
	for num in tmp:
		total = num+total
	return total

all_int = []
ips = []
class Interface(object):
	def __init__(self,device_name,interface_name,input_rate,output_rate,packets_in,packets_out,drop,in_errors,out_errors,ip):
		self.device_name  	= device_name
		self.interface_name	= interface_name
		self.input_rate   	= input_rate
		self.output_rate  	= output_rate
		self.packets_in   	= packets_in
		self.packets_out  	= packets_out
		self.drop         	= drop
		self.in_errors    	= in_errors
		self.out_errors   	= out_errors
		self.ip   			= ip

 
def get_ip (input):
	return(re.findall(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', input))

def make_Interface_object(obj_name,device_name,interface_name,input_rate,output_rate,packets_in,packets_out,drop,in_errors,out_errors,ip):
	obj_name = Interface(device_name,interface_name,input_rate,output_rate,packets_in,packets_out,drop,in_errors,out_errors,ip)
	all_int.append(obj_name)

	

def read_tracert (file_name):
	for line in open(file_name, 'r').readlines():
		line = get_ip(line)
		for ip in line: 
			ips.append(ip)


def read_doc (file_name):
	for line in open(file_name, 'r').readlines():
		my_int.append(line)

to_doc("test2.html","")
def to_doc(file_name, varable):
	f=open(file_name, 'w')
	f.write(varable)
	f.close()
	
def to_doc_a(file_name, varable):
	f=open(file_name, 'a')
	f.write(varable)
	f.close()
	
def to_doc_over_write(file_name, varable):
	f=open(file_name, 'w')
	f.write(varable)
	f.close()


def go_get_CPU(ip):
	try:
		net_connect = netmiko.ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password) 
		tmp_device_info =  net_connect.send_command_expect('show processes cpu | i CPU')
		return tmp_device_info
	except:
		return "Can't SSH to this"

def go_get_info_from_devices(ip):
	try:
		net_connect = netmiko.ConnectHandler(device_type='cisco_ios', ip=ip, username=username, password=password) 
		tmp_device_info =  net_connect.send_command_expect('show int')
		tmp_device_info = tmp_device_info + net_connect.send_command_expect('show processes cpu | i CPU')
		return tmp_device_info
	except:
		return "Can't SSH to this"

username = input("Username: ")
password = getpass() 

read_tracert ('the_tracert.txt')
doc_list = []
for ip in ips:
	my_int = []
	print (my_int)
	doc_name =ip+'int.txt'
	to_doc_over_write (doc_name,go_get_info_from_devices(ip))	
	my_int = []
	doc_list.append(doc_name)
	#go_get_info_from_devices(ip)
			
lines_i_want = ["bits/sec",
				"input error",
				"output error",
				"input packets",
				"packets input",
				"output packets",
				"packets output",
				"drops"]

interface_types = [	"Ethernet[0-9]", 
					"port-channel",
					"Serial",
					"Vlan"]
all_dev = []	
				

for doc in doc_list:
	temp_doc_list = [doc]
	nexus_fix(doc)
	ints_doc=CiscoConfParse(doc)
		
	for interface_type in interface_types:
	#	print (interface_type)
		found_int_type = ints_doc.find_objects(interface_type)
		for interface_type in found_int_type:
			temp_int_list = [interface_type.text]
			temp_sub_int_list = []
			for child in interface_type.all_children:
				for line in lines_i_want:
					if line in child.text:
						temp_sub_int_list.append(child.text)
			temp_int_list.append(temp_sub_int_list)

			temp_dic = {"Interface_Name": 	interface_type.text.split(' ')[0],
						"Interface_line": temp_sub_int_list,
						"Device": 			doc[:-7]}
			all_dev.append (temp_dic)	
			
#for dev in all_dev:
#	print (dev["Device"])
#	print (dev["Interface_Name"])
#	for each in dev["Interface_line"]:
#		print (each)			
		

print ("#################")		
#print (all_dev [0])
for each in all_dev:
	ip = each["Device"]
	
		
	interface_name=each ["Interface_Name"]
	packets_in = 0
	packets_out = 0
	drops = "If this is a Nexus we don't find drops"
	for int_line in each ["Interface_line"]:
		
		if "input rate"	in int_line:
			int_line = int_line.split("input rate")
			int_line = int_line[1].split()[0]
			input_rate =int_line
			
			
		if "output rate" in int_line:
			int_line = int_line.split("output rate")
			int_line = int_line[1].split()[0]
			output_rate =int_line
			
			
		if "input error" in int_line:
			in_errors=find_all_numbers(int_line)
			
		if "output error" in int_line:
			out_errors=find_all_numbers(int_line)
		
		if 'input packets' in int_line:
			int_line = int_line.split()[0]
			if int(int_line) > int(packets_in):
				packets_in = str(int_line)
				
		if 'packets input' in int_line:
			int_line = int_line.split()[0]
			if int(int_line) > int(packets_in):
				packets_in = str(int_line)
		
		if 'output packets' in int_line:
			int_line = int_line.split()[0]
			if int(int_line) > int(packets_out):
				packets_out = str(int_line)
				
		if 'packets output' in int_line:
			int_line = int_line.split()[0]
			if int(int_line) > int(packets_out):
				packets_out = str(int_line)
		
		if "Total output drops:" in int_line:
			start_of_drops = int_line.split("Total output drops:")
			drops = start_of_drops[-1]
			
	print (ip)		
	packets_in = str(packets_in)
	packets_out = str(packets_out)
	obj_name = ip + interface_name
	device_name = ip
	print (interface_name)	
	print ("drops: "+ drops)
	print ("Input Errors: "+str(in_errors))
	print ("Output Error: "+str(out_errors))
	print ("Input Rate: "+str(input_rate))
	print ("Output Rate: "+str(output_rate))
	print ("Packets In: "+str(packets_in))
	print ("Packets out: "+str(packets_out))
	
	make_Interface_object(obj_name,device_name,interface_name,input_rate,output_rate,packets_in,packets_out,drops,str(in_errors),str(out_errors),ip)

from html_crap import *

html_file_name = 'test2.html'

to_doc_a(html_file_name, head)
first_time_though = True

	
for ip in ips:
	if first_time_though == False:
		to_doc_a(html_file_name,next_item)
	first_time_though = False
	temp_ip_cpu = go_get_CPU(ip)
	temp_ip_cpu = ip + '<br>'+temp_ip_cpu 	
	to_doc_a(html_file_name,temp_ip_cpu)
	to_doc_a(html_file_name,'</h4>')
	to_doc_a(html_file_name,'<ul data-role="listview">')	

	for each in all_int:
		print (each.device_name)
		if each.ip == ip:
			in_rate = int(each.input_rate)/1000000
			out_rate = int(each.output_rate)/1000000	
			try:
				out_issues = int(each.drop) + int(each.out_errors)
				out_error_rate = out_issues/int(each.packets_out)
				out_error_rate = out_error_rate*100
				if out_error_rate <.0001:
					out_error_rate = 0
			except:	
				out_error_rate = 0
			try:	
				in_error_rate = int(each.in_errors)/int(each.packets_in)
				in_error_rate = in_error_rate *100
				if in_error_rate <.005:
					in_error_rate = 0
			except:
				in_error_rate = 0
			try:
				interface_info = each.interface_name + ' Mb/s in: '+ str(in_rate) +' Mb/s out: '+str(out_rate) + ' In Error rate: '+str(in_error_rate )+"%" +' In Error rate: '+ str(out_error_rate )+"%"
				if in_rate > .5 or out_rate > .5 or in_error_rate > .005  or out_error_rate > .005:
					to_doc_a(html_file_name, '<li><a href="#">')
					if in_error_rate > .5  or out_error_rate > .5:
						to_doc_a(html_file_name,'<font color="red">')
					to_doc_a(html_file_name,interface_info) 
					if in_error_rate > .5  or out_error_rate > .5:
						to_doc_a(html_file_name,'</font>')
					to_doc_a(html_file_name,'</a></li>') 
					to_doc_a(html_file_name,'\n')
	
			except:
				interface_info = each.interface_name + "failed"
				to_doc_a(html_file_name, '<li><a href="#">')
				to_doc_a(html_file_name,interface_info) 
				to_doc_a(html_file_name,'</a></li>') 
				to_doc_a(html_file_name,'\n')
	



to_doc_a(html_file_name,'</ul>')
to_doc_a(html_file_name,'</div>')
to_doc_a(html_file_name, foot)