#!/usr/bin/python
# -*- coding: utf-8 -*-


# Author: Abaraham Pasamar (apasamar [at] incide [dot] es)
# Date: 2015-12-20
# Description: This script sends an input text file (xmas card or ascii art picture) in several emails (one email per file line). 
#              The line is send as email subject, so it can be read without open the email. 
#              Take into account you cannot define subject email font type !  so no monospaced font can be used :(
# Last update: 2015-12-24
# version: 0.3

# input file should be in reverse order (to see propoerly in inbox). You can use cat file | tail -r to reverse file.
# Example1:
#________________0100________________Xmas___
#_______1001☆01001110☆0100001☆1_____Merry___
#________0100☆100101☆000100☆01______Navidad_
#__________00010☆10110110☆10________feliz___
#____________110☆111101☆10___________una____
#_____________11000110☆_____________desea___
#_______________☆0001________________le_____
#_________________☆________________INCIDE___
#____________________________________________


# Take limits into account if you arre going to spam people :). You will send several emails per address (addresses x number of lines )
# consider to use mailchimp. 
# Gmail limits : https://support.google.com/a/answer/166852?hl=es

# If you want to send also a body splitted message, use a ; splitted input file and use split funtion .split(';')

import smtplib
import sys
import base64
import datetime
import time
from socket import gaierror 
import argparse

####### FUNCTIONS ######

def login_account():
	try:
		smtp_conn.login(smtp_user, smtp_password)
	except (smtplib.SMTPException, gaierror), error:
		print str(error)

def logout_account():
	smtp_conn.quit()

def send_email(smtp_user, smtp_receiver, subject, cleansubject,message):
	msg = "From: \"+email_from_name+\"<%s>\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (smtp_user, smtp_receiver, subject)
	msg += message + "\r\n"
	# Send email
	try:
		smtp_conn.sendmail(smtp_user, smtp_receiver, msg)
		g.write(smtp_receiver+": OK -> "+cleansubject+" - "+subject+" \n")
		print smtp_receiver+": OK -> "+cleansubject+" - " +subject
		return True
	except (smtplib.SMTPException, gaierror), error:
		print str(error)
		g.write("*** "+str(error)+" ***\n")
		g.write(smtp_receiver+": FAIL\n")
		print smtp_receiver+": FAIL"
		print "sleeping 180 seconds"
		time.sleep(180)
		return False

#########################


# main()

### arg parse ### 

parser = argparse.ArgumentParser(description='Send xmas card (split multiple emails) to user or userlist')
parser.add_argument('card', help='card file to sent')
parser.add_argument('-e', '--email', help='receiver email address')
parser.add_argument('-l','--list', help='list of email addresses')
args = parser.parse_args()


if (args.email==None and args.list==None):
	print "Please, an email address or a list is needed"
	sys.exit()

### server and port
smtp_server = 'smtp.gmail.com'
smtp_port= '587'

### account ####

#smtp_user = 'xxxxxx@xxxxxxx.xxx'
#smtp_password = 'xxxxxxxxxxxxxxxx'



### receiver ####
smtp_receiver = args.email

email_from_name="Abraham Pasamar (INCIDE)"


# verify args...

print "receiver: "+str(smtp_receiver)
print "file: "+args.card
print "receivers file_list: "+str(args.list)


### Email subject
# File lines

### Email content
message = '\n'

# log file
g=open('log.txt','a')


f=open(args.card,'r') #############  arg parser

data=f.readlines()

### smtp initilize
smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
smtp_conn.starttls() # tls !

#### login
login_account()

# list of addresses

if args.list:
	h=open(args.list,'r')
	mytmp=h.readlines()
	mylist=[]
	for item in mytmp:
		mylist.append(item.rstrip())

else:           # not list, single address
	mylist=[]
	mylist.append(smtp_receiver)

## mail loop : addresses
for address in mylist:
	#log 
	g.write("======= NewSession ========\n")
	print "======= NewSession ========"

	g.write("Date: "+str(datetime.datetime.now())+"\n")
	print "Date: "+str(datetime.datetime.now())

	g.write(str(address)+"\n")
	print address

	send_check=False
	# second loop (check if email connection/sending fails)
	while send_check==False:
		for line in data:    #  file lines loop
			tmp=line.rstrip() # remove \n
			subject='=?utf-8?B?'+base64.b64encode(tmp)+'?='   # use utf8 encoding
			send_check=send_email(smtp_user, address, subject, tmp,message)      #### send email (file line)
			# sleep
			time.sleep(0.5) # between lines (0,5 seconds sleep)
			if send_check==False: 
				break
	time.sleep(5) # between addresses (avoid rate smtp limit)  
 
######


### logout
logout_account()

f.close()
g.close()

