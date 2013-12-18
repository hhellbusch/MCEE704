#!/usr/bin/python

import smtplib
import os

sender = 'notify@phalanx.rit.edu'
receivers = ['hhellbusch@gmail.com']


pathname = os.path.dirname(os.path.realpath(__file__))

message = """From: notify <notify@phalanx.rit.edu>
To: To Henry <hhellbusch@gmail.com>
Subject: finfet is done simming!

""" + pathname + """"
yoyyoo its finally done. go check the results .
"""

try:
	smtpObj = smtplib.SMTP('localhost')
	smtpObj.sendmail(sender, receivers, message)
except SMTPException:
	print "Error: unable to send email!"
