#
# Nancy Minyanou
# Date of creation: 8-27-16
# Last modified:
# Built on Python 3.5.2
#
# Based on http://naelshiab.com/tutorial-send-email-python/
#
# Checks if its Monday, if so send the report from last week to myself
#

import smtplib
from email import *
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import time
import os
import sys
from tkinter import *

root = Tk()
root.wm_title("Enter email addreses and password.")
root.wm_attributes("-topmost", 1)


class requestEmailPass():

    def __init__(self, master):
        self.master = master
        self.mainFrame = Frame(self.master)
        self.mainFrame.grid(row=0, column=0)

        self.directions = Label(self.mainFrame)
        self.directions.configure(
            text="Enter the gmail address to send report\nfrom and its password along with\nemail address to send report to.")
        self.directions.grid(row=0, column=0, columnspan=2)

        self.fromaddr_label = Label(self.mainFrame)
        self.fromaddr_label.configure(text="From email:")
        self.fromaddr_label.grid(row=1, column=0, sticky=W)

        self.pw_label = Label(self.mainFrame)
        self.pw_label.configure(text="Password:")
        self.pw_label.grid(row=2, column=0, sticky=W)

        self.toaddr_label = Label(self.mainFrame)
        self.toaddr_label.configure(text="To email:")
        self.toaddr_label.grid(row=3, column=0, sticky=W)

        self.fromaddr_entry = Entry(self.mainFrame, width=30)
        self.fromaddr_entry.grid(row=1, column=1)
        self.fromaddr_entry.focus_set()

        self.pw_entry = Entry(self.mainFrame)
        self.pw_entry.grid(row=2, column=1)
        self.pw_entry.configure(show="*", width=30)

        self.toaddr_entry = Entry(self.mainFrame, width=30)
        self.toaddr_entry.grid(row=3, column=1)

        self.btn_done = Button(
            self.mainFrame, text='Done', command=self.saveInfo)
        self.btn_done.grid(row=4, column=0, columnspan=2)
        self.btn_done.bind("<Return>", self.saveInfo)

    def saveInfo(self):
        self.fromaddr = self.fromaddr_entry.get()
        self.toaddr = self.toaddr_entry.get()
        self.pw = self.pw_entry.get()
        print(len(sys.argv))
        self.report = SendReport(self.fromaddr, self.toaddr, self.pw, sys.argv[1], sys.argv[2])
        self.master.destroy()


class SendReport(object):
    def __init__(self, fromaddr, toaddr, pw, lastweek, thisweek):
        print("the last week was " + lastweek)
        print("this week is " + thisweek)
        try:

            self.fromaddr = fromaddr
            self.toaddr = toaddr
            self.pw = pw

            self.msg = MIMEMultipart()

            self.msg['From'] = self.fromaddr
            self.msg['To'] = self.toaddr

            self.week = int(str(time.strftime("%U"))) - 1
            self.year = time.strftime("%Y")

            self.full_datetime = time.strptime(
                '{} {} 1'.format(self.year, self.week), '%Y %W %w')

            self.datetime = str(
                self.year + "_WeekOf-" + str(self.full_datetime.tm_mon) + "-" + str(self.full_datetime.tm_mday))

            self.msg['Subject'] = "TaskList from week " + str(self.full_datetime.tm_mon) + "-" + str(
                self.full_datetime.tm_mday)

            self.body = "Summarize and report to Juhi"

            self.msg.attach(MIMEText(self.body, 'plain'))

            self.filename = lastweek + ".csv"
            self.attachment = open("Tasks_csv\\" + self.filename, "rb")

            self.part = MIMEBase('application', 'octet-stream')
            self.part.set_payload(self.attachment.read())
            encoders.encode_base64(self.part)
            self.part.add_header('Content-Disposition',
                                 "attachment; filename= %s" % self.filename)

            self.msg.attach(self.part)

            self.server = smtplib.SMTP('smtp.gmail.com', 587)
            self.server.starttls()
            self.server.login(self.fromaddr, self.pw)
            self.text = self.msg.as_string()
            self.server.sendmail(self.fromaddr, self.toaddr, self.text)

            self.server.quit()
            self.attachment.close()

            self.oldpath = "Tasks_csv/" + self.filename
            self.newpath = "Tasks_sent_csv/" + self.filename

            os.rename(self.oldpath, self.newpath)

        except FileNotFoundError:
            print("already sent")


def start():
    app = requestEmailPass(root)
    root.mainloop()


if __name__ == '__main__':
    start()
