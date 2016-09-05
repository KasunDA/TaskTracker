# Nancy Minyanou
# Date of Creation: 8-23-2016
# Last modification: 9-05-2016
#
# Built on Python 3.5.2 32-Bit
#
# todo: add view by week option
# todo: add export to by week option

import csv
import os
import time
import sqlite3

from tkinter import *

root = Tk()
root.wm_title("Task List")
root.wm_attributes("-topmost", 1)


class UserForm:
    cur = None
    thisweek = None
    conn = None

    def __init__(self, master):
        global cur
        global thisweek
        global conn

        self.master = master

        self.mainlabelframe = LabelFrame(self.master, text="Directions")
        self.mainlabelframe.grid(column=0, row=0, columnspan=3)

        self.directions = Label(self.mainlabelframe,
                                text="Click the dropdown list to select the time interval\n"
                                     "to request what you're doing.\n"
                                     "Click start to start recording\n"
                                     "On Mondays the previous week's report will be emailed.")
        self.directions.grid(column=1, row=0)

        self.options = LabelFrame(self.master, text="Options")
        self.options.grid(column=0, row=1, columnspan=3)

        # place label and drop down for selecting time interval
        self.label_time = Label(
            self.options, text="Select time interval (mins) for notification:")
        self.label_time.grid(row=0, column=0)

        # todo: add listener so it updates interval when dropdown choice
        # changes
        self.time_options = [
            "1",
            "5",
            "15",
            "30",
            "45",
            "60",
            "90"
        ]

        self.time_interval = IntVar(self.master)
        self.time_interval.set(self.time_options[0])

        self.dropdown_time_intervals = OptionMenu(
            self.options, self.time_interval, *self.time_options)
        self.dropdown_time_intervals.grid(column=1, row=0, sticky=E + W)

        self.userTask = None

        self.year = time.strftime("%Y")
        self.week = time.strftime("%U")

        self.full_datetime = time.strptime(
            '{} {} 1'.format(self.year, self.week), '%Y %W %w')

        self.datetime = str(self.full_datetime.tm_year) + "_WeekOf-" + str(self.full_datetime.tm_mon) + "-" + str(
            self.full_datetime.tm_mday)

        self.last_update = ""

        self.tasks_folder = "Tasks_csv"
        self.tests_sent_folder = "Tasks_sent_csv"
        os.makedirs(self.tasks_folder, exist_ok=True)
        os.makedirs(self.tests_sent_folder, exist_ok=True)

        self.tasks_csv_path = self.tasks_folder + "/" + self.datetime + '.csv'

        # at the start of task tracking, repeat request for user input at
        # specified interval and update the main window
        # to show last time request was made.
        # Create the csv for the week if it doesn't already exist
        def entryForm(shouldRun, interval, name):
            self.last_update = time.strftime("%a %I:%M %p")
            self.label_last_update.configure(
                text="Time of last update: " + self.last_update)

            if name == "Start":
                self.shouldRun = True
                self.name = "Start"
                self.btn_start.configure(state="disabled")
                self.btn_stop.configure(state="normal")
                self.first_time = False

                tempTime = time.strftime("%a %I:%M %p")
                cur.execute("""INSERT INTO WeeklyReportRaw (week, datetime, tasks) VALUES (?, ?, 'Start')""",
                            (thisweek, tempTime))
                conn.commit()

            if self.shouldRun:
                self.userTask = popupWindow(self.master, interval, shouldRun)
                master.wait_window(self.userTask.top)

                # add entry to database
                whatdoing = entryValue(self)
                tempTime = time.strftime("%a %I:%M %p")
                cur.execute("""INSERT INTO WeeklyReportRaw (week, datetime, tasks, forwho) VALUES (?, ?, ?, ?)""",
                            (thisweek, tempTime, whatdoing[0], whatdoing[1]))
                conn.commit()

                self.master.after(interval, lambda: entryForm(
                    shouldRun, interval, ""))

        self.old_value = ""
        self.old_forwho = ""

        # get the user's entered value
        # if nothing was entered, use the last value
        def entryValue(self):
            if self.userTask.value:
                self.old_value = self.userTask.value
            if not self.userTask.value:
                self.userTask.value = self.old_value

            if self.userTask.forwho:
                self.old_forwho = self.userTask.forwho
            if not self.userTask.forwho:
                self.userTask.forwho = self.old_forwho

            return self.userTask.value, self.userTask.forwho

        # when the user stops, timestamp the stopping point
        # and disable the request for user input
        # todo: disable dropdown when start, enable when stopping
        def changeRun(self):
            self.btn_start.configure(state="normal")
            self.btn_stop.configure(state="disabled")
            self.shouldRun = False
            self.name = "Stop"

            tempTime = time.strftime("%a %I:%M %p")
            cur.execute("""INSERT INTO WeeklyReportRaw (week, datetime, tasks) VALUES (?, ?, 'Stop')""",
                        (thisweek, tempTime))
            conn.commit()

        self.shouldRun = True
        self.name = "Start"
        self.first_time = True

        # label for time of last update on root window
        self.label_last_update = Label(self.options)
        self.label_last_update.configure(
            text="Time of last update: " + self.last_update)
        self.label_last_update.grid(row=1, column=0, columnspan=2)

        # start button
        self.btn_start = Button(self.options, text="Start",
                                command=lambda: entryForm(self.shouldRun, self.time_interval.get() * 60000, "Start"))
        self.btn_start.grid(column=0, row=2, sticky=W + E, columnspan=2)

        # stop button
        self.btn_stop = Button(self.options, text="Stop",
                               command=lambda: changeRun(self))
        self.btn_stop.grid(column=0, row=3, sticky=W + E, columnspan=2)
        self.btn_stop.configure(state="disabled")

    def loadDataBase(self, lthisweek, lastweek):
        global cur
        global conn
        global thisweek

        thisweek = lthisweek
        if not os.path.isfile("data.sqlite3"):
            conn = sqlite3.connect('data.sqlite3')
            cur = conn.cursor()

            cur.execute('DROP TABLE IF EXISTS WeeklyReportRaw')
            cur.execute('CREATE TABLE WeeklyReportRaw (week TEXT, datetime TEXT, tasks TEXT, forwho TEXT)')
            print("database doesn't exist")
        elif os.path.isfile("data.sqlite3"):
            print("database exists")
            conn = sqlite3.connect('data.sqlite3')
            cur = conn.cursor()

# popup window that asks for user input
# appears centered on screen and destroys itself if user doesn't
# press done after 5 minutes


class popupWindow(Tk):

    def __init__(self, master, interval, shouldRun):
        top = self.top = Toplevel(master)
        top.wm_attributes("-topmost", 1)

        # center the window
        width_screen = root.winfo_screenwidth()  # width of the screen
        height_screen = root.winfo_screenheight()  # height of the screen

        w = 300  # width for the Tk root
        h = 200  # height for the Tk root

        # calculate x and y coordinates for the Tk root window
        x = (width_screen / 2) - (w / 2)
        y = (height_screen / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        top.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.interval = interval

        self.shouldRun = shouldRun

        self.master = master

        # label for prompting user input
        self.label_question = Label(
            self.top, text="What are you doing right now?\nTime Now: " + time.strftime("%I:%M:%S %p"))
        self.label_question.pack()

        # text box for user input, sets focus on self when window appears
        self.userTaskInput = Text(self.top)
        self.userTaskInput.config(width=30, height=5)
        self.userTaskInput.focus_set()
        self.userTaskInput.pack()

        self.label_forwho = Label(self.top, text="Who are you doing this for?")
        self.label_forwho.pack()

        self.userTaksInput_forwho = Entry(self.top)
        self.userTaksInput_forwho.pack()

        # closes the window upon click/enter of Done
        self.btn_done = Button(self.top, text='Done', command=self.cleanup)
        self.btn_done.pack()
        self.btn_done.bind("<Return>", self.cleanup)

        top.protocol("WM_DELETE_WINDOW", self.cleanup)

        # close the window if user doesn't hit "done" within 5 mins
        self.top.after(300000, self.cleanup)

    def stop(self):
        self.shouldRun = False

    def cleanup(self):
        self.value = self.userTaskInput.get("1.0", "end-1c")
        self.forwho = self.userTaksInput_forwho.get()
        self.top.destroy()


if __name__ == '__main__':
    # todo: add command line so can pass in file name to report to send_csv.py

    # this year
    year = time.strftime("%Y")
    # last week
    last_week = int(str(time.strftime("%U"))) - 1  # previous week
    last_week_full_datetime = time.strptime(
        '{} {} 1'.format(year, last_week), '%Y %W %w')
    last_week_datetime_title = str(
        year + "_WeekOf-" + str(last_week_full_datetime.tm_mon) + "-" + str(last_week_full_datetime.tm_mday))

    # this week
    this_week = int(str(time.strftime("%U")))  # this week
    this_week_full_datetime = time.strptime(
        '{} {} 1'.format(year, this_week), '%Y %W %w')
    this_week_datetime_title = str(
        year + "_WeekOf-" + str(this_week_full_datetime.tm_mon) + "-" + str(this_week_full_datetime.tm_mday))

    if time.strftime("%a") == "Mon":
        if os.path.isfile("Tasks_csv\\" + last_week_datetime_title + '.csv'):
            # calls send csv to send out if its monday
            os.system('Python send_csv.py')

    app = UserForm(root)

    # todo: replace csv structure with SQL database
    app.loadDataBase(this_week_datetime_title, last_week_datetime_title)

    root.mainloop()
