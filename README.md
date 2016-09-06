# TaskList
Utility to track what you're doing at user specified intervals. At the startup on a Monday it emails out the last week's report to user specified email address from user's gmail.

## Background
One of my supervisors at work asked me to turn in some sort of log or sumary of my daily activity on a weekly basis. I wasn't sure the best way to go about this so I created this utility. Basically I knew I wanted to do the following:
* Output to some sort of text file or database.
* Ability to start and stop tracking.
* A utility that would be mildly intrusive and force me to be mindful about what I'm doing and for whom I'm doing it.
* A reminder to compile these personal notes for my supervisor. 

This was developed on a 64-bit Windows 10 PC with Python 3.5.2

## User Guide
All that is needed to run is the TaskTracker.py and send_csv.py files. 
'
Start TaskTracker.py, select your time interval, hit start to start the reminders and stop to stop them. On Mondays, input your email, the "to" email, and expect an email of last week's reports.

### TaskTracker.py
This is the bulk of the program. Using Tkinter for Python 3, it presents the user with a window to select the time interval in which they want to be asked to submit an entry (1, 5, 10, 15, 30, 45, 60, or 90 minutes). 

The "Start" starts the application and creates a record in the SQLite with the along with an identifier for that week. For example: 2016_WeekOf-8-22 corresponds to the 34th week of the year and 8-22 is the Monday of that week.

The user enters what they are doing and for whom it is in the popup-dialogue. This popup closes itself after 5 minutes. If the entry is empty, it assumes the last task entered is the task still being worked on and adds the same task to the csv. This is because I personally step away from my computer with irregular frequency so if I didn't respond to it it is very likely I"m still working on the last thing I entered.

"Stop" ends the tracking. Each Start/Stop is also timestampped in the SQLite database.

Each record added goes into the same SQLite database
### send_csv.py
If it is a Monday when the TaskTracker.py program is started, the app asks for the following:
* "From" gmail address of the user
* "Password" of the user's gmail
* "To" email address to send the last week's task report to

It then moves the last week's report to a folder for already sent reports. If it doesn't find an appropriate file for the last week, it currently assumes that it has already been sent. 

## Future Features
A few things I'd like to implement to flesh this out:
* Validate email addresses
* Expand to more than just gmail addresses
* Some way to filter or summarize the entries from the emailed report (word or phrase frequency count?)
* Have mutliple users and profiles
* Host entries on a remote server instead of locally maybe
