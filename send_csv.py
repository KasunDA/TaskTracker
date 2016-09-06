#
# Nancy Minyanou
# Date of creation: 8-27-16
# Last modified:
# Built on Python 3.5.2
#
# Based on http://naelshiab.com/tutorial-send-email-python/
#
# Sends condensed version of last week's report:
# message body::
# Summary of the last week's activity::
# Mon:
#         testing again
#         asdfasda qw42 teg
#         just sent a thing
#         again
#         a
#         b
# Tues:
#         testing again who cares
#         b
# Wens:
#         fixed the emailing unique tasks part
# Thurs:
#
# Friday:
#
# todo: add "sent" table to keep track of reports that were already sent to prevent dialogue from popping up on every start on a Monday
#
#
import smtplib
import sqlite3
from collections import OrderedDict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import *

root = Tk()
root.wm_title("Enter email addreses and password.")
root.wm_attributes("-topmost", 1)


# popup dialogue that takes in user's email/password and to-email to send last week's report
# as a summary of the sql records pertaining to last week
class requestEmailPass():
    def __init__(self, master):
        self.master = master
        self.mainFrame = Frame(self.master)
        self.mainFrame.grid(row=0, column=0)

        self.directions = Label(self.mainFrame)
        self.directions.configure(
            text="Enter the gmail address to send report\nfrom and its password along with"
                 "\nemail address to send report to.\n"
                 "If you do not wish to send the report, press cancel.")
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
        self.btn_done.grid(row=4, column=0, columnspan=2, sticky=W, padx=70, pady=10)
        self.btn_done.bind("<Return>", self.saveInfo)

        self.btn_cancel = Button(
            self.mainFrame, text='Cancel', command=lambda: self.master.destroy())
        self.btn_cancel.grid(row=4, column=0, columnspan=2, sticky=E, padx=70, pady=10)
        self.btn_cancel.bind("<Return>", lambda x: self.master.destroy())

    # function to store email/password info and start report sending
    def saveInfo(self):
        self.fromaddr = self.fromaddr_entry.get()
        self.toaddr = self.toaddr_entry.get()
        self.pw = self.pw_entry.get()
        self.report = SendReport(self.fromaddr, self.toaddr, self.pw, sys.argv[1], sys.argv[2])
        self.master.destroy()


class SendReport(object):
    cur = None
    conn = None

    def __init__(self, fromaddr, toaddr, pw, lastweek, thisweek):
        global conn
        global cur

        conn = sqlite3.connect('data.sqlite3')
        cur = conn.cursor()

        self.fromaddr = fromaddr
        self.toaddr = toaddr
        self.pw = pw
        self.lastweek = lastweek
        self.thisweek = thisweek

        cur.execute("""SELECT datetime, tasks, forwho
                        FROM WeeklyReportRaw
                        WHERE week LIKE (?)
                        AND (tasks NOT LIKE 'Start')
                        AND (tasks NOT LIKE 'Stop')""", [self.thisweek])
        report = (cur.fetchall())

        weekly_summary = {'Mon': [], 'Tues': [], 'Wens': [], 'Thurs': [], 'Fri': [], 'Sat': [], 'Sun': []}

        # each day of the week is a list for each key in the weekly summary dictionary for easy retrieval
        for row in report:
            if re.search('Mon', str(row)):
                weekly_summary['Mon'].append(row)
            if re.search('Tues', str(row)):
                weekly_summary['Tues'].append(row)
            if re.search('Wens', str(row)):
                weekly_summary['Wens'].append(row)
            if re.search('Thurs', str(row)):
                weekly_summary['Thurs'].append(row)
            if re.search('Fri', str(row)):
                weekly_summary['Fri'].append(row)
            if re.search('Sat', str(row)):
                weekly_summary['Sat'].append(row)
            if re.search('Sun', str(row)):
                weekly_summary['Sun'].append(row)

        def getKey(item):
            return item[0]

        # todo: find a more efficient way to store the weekly data than by day individally
        # each day of the week gets condensed to just the unique activities for that day of the week, listed by
        # order of entry
        # monday data
        mon_set = list(set(weekly_summary['Mon']))

        mon_set = sorted(mon_set, key=getKey)

        map(str, mon_set)

        mon_set_key = [x[1] for x in mon_set]
        mon_set_val = [x[2] for x in mon_set]

        mon_set_dict = OrderedDict(zip(mon_set_key, mon_set_val))

        # tuesday data
        tues_set = list(set(weekly_summary['Tues']))

        tues_set = sorted(tues_set, key=getKey)

        map(str, tues_set)

        tues_set_key = [x[1] for x in tues_set]
        tues_set_val = [x[2] for x in tues_set]

        tues_set_dict = OrderedDict(zip(tues_set_key, tues_set_val))

        # wenesday data
        wens_set = list(set(weekly_summary['Wens']))

        wens_set = sorted(wens_set, key=getKey)

        map(str, wens_set)

        wens_set_key = [x[1] for x in wens_set]
        wens_set_val = [x[2] for x in wens_set]

        wens_set_dict = OrderedDict(zip(wens_set_key, wens_set_val))

        # thursday data
        thurs_set = list(set(weekly_summary['Thurs']))

        thurs_set = sorted(thurs_set, key=getKey)

        map(str, thurs_set)

        thurs_set_key = [x[1] for x in thurs_set]
        thurs_set_val = [x[2] for x in thurs_set]

        thurs_set_dict = OrderedDict(zip(thurs_set_key, thurs_set_val))

        # thursday data
        fri_set = list(set(weekly_summary['Fri']))

        fri_set = sorted(fri_set, key=getKey)

        map(str, fri_set)

        fri_set_key = [x[1] for x in fri_set]
        fri_set_val = [x[2] for x in fri_set]

        fri_set_dict = OrderedDict(zip(fri_set_key, fri_set_val))

        # create the condensed report as the body of the email
        messagebody = "Mon:\n\t" + '\n\t'.join(mon_set_dict)
        messagebody += "\nTues:\n\t" + '\n\t'.join(tues_set_dict)
        messagebody += "\nWens:\n\t" + '\n\t'.join(wens_set_dict)
        messagebody += "\nThurs:\n\t" + '\n\t'.join(thurs_set_dict)
        messagebody += "\nFriday:\n\t" + '\n\t'.join(fri_set_dict)

        self.msg = MIMEMultipart()

        self.msg['From'] = self.fromaddr
        self.msg['To'] = self.toaddr

        self.msg['Subject'] = "TaskList from week " + self.lastweek

        self.body = "Summary of the last week's activity:\n\n" + messagebody

        self.msg.attach(MIMEText(self.body, 'plain'))

        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.server.starttls()
        self.server.login(self.fromaddr, self.pw)
        self.text = self.msg.as_string()
        self.server.sendmail(self.fromaddr, self.toaddr, self.text)

        self.server.quit()


def start():
    app = requestEmailPass(root)
    root.mainloop()


if __name__ == '__main__':
    start()
