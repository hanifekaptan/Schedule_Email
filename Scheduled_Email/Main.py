# Author: Hanife Kaptan

# Description: It is an application that allows you to send a post-dated letter via e-mail on the target date.

# version: Python (3.11.2), PyQt5 (5.15.10), PyQt5Designer (5.14.1), psycopg2 (2.9.6)


import time
import schedule
from PyQt5.QtWidgets import QApplication
from App import App
from Task import Task

app = QApplication([])
window = App()
window.show()
app.exec_()
window.sp.disconnect()
task = Task()

schedule.every().minutes.do(task.proccess)

while True:
    schedule.run_pending()
    time.sleep(30)
    if task.isTableEmpty() == True:
        break
