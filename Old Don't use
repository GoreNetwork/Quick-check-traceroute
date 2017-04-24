from tkinter import *
from tkinter import ttk
import random
import os
import re
import socket
import sys
import netmiko
import time
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

def no_extra_spaces(line):
	lst = ""
	for each_letter in line:
		if each_letter != " ":
			lst=lst+each_letter
		if each_letter == " ":
			lst=lst+" "
	for pound in lst:
		lst = lst.replace("  ", " ")
	return lst

def no_inital_space(line):
    if line[0] == " ":
        return line[1:]
    else:
        return line

def remove_return(entry):
	tmp = entry.rstrip('\n')
	return tmp

def read_tracert (file_name):
	for line in open(file_name, 'r').readlines():
		line = get_ip(line)
		for ip in line: 
			ips.append(ip)


def read_doc (file_name):
	for line in open(file_name, 'r').readlines():
		my_int.append(line)

def to_doc(file_name, varable):
	f=open(file_name, 'a')
	f.write(varable)
	f.close()
	
def to_doc_over_write(file_name, varable):
	f=open(file_name, 'w')
	f.write(varable)
	f.close()

def add_numbers(line):
    temp = []
    for s in line.split():
        if s.isdigit():
            temp.append(s)
    total = 0
    for number in temp:
        total = total + int(number)
    return total

def find_output_errors(line):
    temp = []
    for s in line.split():
        if s.isdigit():
            temp.append(s)
    total = 0
    for number in temp[:1]:
        total = total + int(number)
    return total

def go_get_CPU(ip):
	try:
		net_connect = netmiko.ConnectHandler(device_type='cisco_ios', ip=ip, username='username', password='password') 
		tmp_device_info =  net_connect.send_command_expect('show proc cpu | i CPU utilization for')
		return tmp_device_info
	except:
		return "Can't SSH to this"

def go_get_info_from_devices(ip):
	try:
		net_connect = netmiko.ConnectHandler(device_type='cisco_ios', ip=ip, username='username', password='password') 
		tmp_device_info =  net_connect.send_command_expect('show int')
		tmp_device_info = tmp_device_info + net_connect.send_command_expect('show proc cpu | i CPU utilization for')
		return tmp_device_info
	except:
		return "Can't SSH to this"

read_tracert ('the_tracert.txt')

interface_types = ['astEthernet','igabitEthernet','enGigabitEthernet','Vlan','erial','ultilink','unnel']
all_int = []


for ip in ips:
	my_int = []
	print (my_int)
	doc_name =ip+'int.txt'
	to_doc_over_write (doc_name,go_get_info_from_devices(ip))	
	my_int = []
	read_doc (doc_name)				
	for line in my_int:
		for interface in interface_types:
			if interface in line:
				line = line.split(' ')
				int_name = line[0]
				int_name = remove_return(int_name)
				int_name = remove_return(int_name)
				int_name = remove_return(int_name)
				#print (int_name)
		if "input rate" in line:
			start_of_input_rate = line.index("input rate")+11
			end_of_input_rate = line[start_of_input_rate:].index(" ")
			input_rate = line[start_of_input_rate:start_of_input_rate+end_of_input_rate]
		if "output rate" in line:
			start_of_output_rate = line.index("output rate")+12
			end_of_output_rate = line[start_of_output_rate:].index(" ")
			output_rate = line[start_of_output_rate:start_of_output_rate+end_of_output_rate]
		if "packets input" in line:
			line = no_extra_spaces(line)
			line = no_inital_space(line)
			line = line.split (' ')
			packets_in = line [0]
		if "packets output" in line:
			line = no_extra_spaces(line)
			line = no_inital_space(line)
			line = line.split (' ')
			packets_out = line [0]
		if "input errors" in line:
			in_errors = add_numbers(line)
		if 'output drops' in line:
			line = remove_return(line)
			line = line.split(' ')
			drops = line[-1]
		if "output errors" in line:
			out_errors = find_output_errors(line)
			obj_name = ip + int_name
			device_name = ip
		if "line" in line:
			try:
				make_Interface_object(obj_name,device_name,int_name,input_rate,output_rate,packets_in,packets_out,drops,str(in_errors),str(out_errors),ip)
			except:
				print ("didn't work")
	try:
		make_Interface_object(obj_name,device_name,int_name,input_rate,output_rate,packets_in,packets_out,drops,str(in_errors),str(out_errors),ip)
	except:
				print ("didn't work")		

from html_crap import *



html_file_name = 'test2.html'

first_time_though = True
to_doc(html_file_name, head)
for ip in ips:
	if first_time_though == False:
		to_doc(html_file_name,next_item)
	first_time_though = False
	temp_ip_cpu = go_get_CPU(ip)
	temp_ip_cpu = ip + '<br>'+temp_ip_cpu 	
	to_doc(html_file_name,temp_ip_cpu)
	to_doc(html_file_name,'</h4>')
	to_doc(html_file_name,'<ul data-role="listview">')
	for each in all_int:
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
				if in_error_rate <.0001:
					in_error_rate = 0
			except:
				in_error_rate = 0
			try:
				interface_info = each.interface_name + ' Mb/s in: '+ str(in_rate) +' Mb/s out: '+str(out_rate) + ' In Error rate: '+str(in_error_rate )+"%" +' In Error rate: '+ str(out_error_rate )+"%"
				if in_rate > .5 or out_rate > .5 or in_error_rate > .005  or out_error_rate > .005:
					to_doc(html_file_name, '<li><a href="#">')
					if in_error_rate > .5  or out_error_rate > .5:
						to_doc(html_file_name,'<font color="red">')
					to_doc(html_file_name,interface_info) 
					if in_error_rate > .5  or out_error_rate > .5:
						to_doc(html_file_name,'</font>')
					to_doc(html_file_name,'</a></li>') 
					to_doc(html_file_name,'\n')

			except:
				interface_info = each.interface_name + "failed"
				to_doc(html_file_name, '<li><a href="#">')
				to_doc(html_file_name,interface_info) 
				to_doc(html_file_name,'</a></li>') 
				to_doc(html_file_name,'\n')
	



to_doc(html_file_name,'</ul>')
to_doc(html_file_name,'</div>')
to_doc(html_file_name, foot)
