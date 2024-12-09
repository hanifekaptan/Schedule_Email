import datetime
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from AppWindow import Ui_MainWindow
from Settings import Settings

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.sp = Settings()
        
        self.begginingProccess()
        self.sp.ui.saveB.clicked.connect(self.updatesEmailList)
        self.sp.ui.addB.clicked.connect(self.updatesEmailList)
        self.sp.ui.deleteB.clicked.connect(self.updatesEmailList)
        self.ui.settingsB.clicked.connect(self.openSettings)
        self.ui.writeB.clicked.connect(self.openLetter)
        self.ui.emailsForSend.currentIndexChanged.connect(self.greeting)
        self.ui.sendB.clicked.connect(self.control)
        self.ui.backHomeB.clicked.connect(self.backHomePage)
        
    def begginingProccess(self):
        """
        Basic operations when the application is started.
        """
        self.ui.dateTime.setMinimumDateTime(datetime.datetime.now())
        self.ui.emailsForSend.addItems(self.sp.mails())
        self.ui.emailsForSend.setCurrentText(self.sp.defaultMail())
        self.sp.cur.execute('SELECT "name" FROM settings_info WHERE "default_v" = true')
        name = self.sp.toConvertValidFormat(self.sp.cur.fetchone())
        self.sp.cur.execute('SELECT "lastname" FROM settings_info WHERE "default_v" = true')
        lastname = self.sp.toConvertValidFormat(self.sp.cur.fetchone())
        self.ui.letter.setText("\tDear "+ name.capitalize()+ " "+ lastname.capitalize()+ ",\n")

    def updatesEmailList(self):
        """
        Method that updates the email list in the Letter Page after inserting and deleting operations.
        """
        self.ui.emailsForSend.clear()
        self.ui.emailsForSend.addItems(self.sp.mails())
        self.ui.emailsForSend.setCurrentText(self.sp.defaultMail())

    def openSettings(self):
        """
        Method that opens the Settings Window.
        """
        self.sp.show()
        self.sp.ui.settings.setCurrentIndex(0)

    def openLetter(self):
        """
        Method that opens the Letter Page.
        """
        self.ui.application.setCurrentIndex(1)

    def greeting(self):
        """
        Method that changes the content of the e-mail when the selected e-mail address changes in the Letter Page.
        """
        lettList = list(self.ui.letter.toPlainText().partition("\n"))
        email = self.ui.emailsForSend.currentText()
        self.sp.cur.execute('SELECT "name" FROM settings_info WHERE "email" = %s', (email,))
        name = self.sp.toConvertValidFormat(self.sp.cur.fetchone())
        self.sp.cur.execute('SELECT "lastname" FROM settings_info WHERE "email" = %s', (email,))
        lastname = self.sp.toConvertValidFormat(self.sp.cur.fetchone())
        lettList[0] = "\tDear "+ name.capitalize()+ " "+ lastname.capitalize()+ ",\n"
        self.ui.letter.setText(lettList[0]+lettList[2])

    def control(self):
        """
        Method that checks whether the information and email are NaN and whether the time is in the past or present.
        """
        if self.isFull() == False:
            self.noneValueError()
        elif self.isPastOrNow() == True:
            self.timeError()
        elif self.sp.isListEmpty() == True:
            self.sp.emptyListError()
        else:
            self.sp.cur.execute('SELECT "name" FROM settings_info WHERE "email" = %s',(self.ui.emailsForSend.currentText(),))
            name = self.sp.toConvertValidFormat(self.sp.cur.fetchone())
            self.sp.cur.execute('SELECT "lastname" FROM settings_info WHERE "email" = %s',(self.ui.emailsForSend.currentText(),))
            lastname = self.sp.toConvertValidFormat(self.sp.cur.fetchone())
            self.confirmation(name+" "+lastname, self.ui.dateTime.dateTime().toPyDateTime())

    def addData(self):
        """
        Method that adds datas to the letter_info table after the letter is sent.
        """
        self.sp.cur.execute('INSERT INTO letter_info VALUES (%s, %s, %s, %s, %s);', (self.idValue()+1,
            self.ui.dateTime.dateTime().toPyDateTime(), self.ui.emailsForSend.currentText(),
            self.ui.title.text(), self.ui.letter.toPlainText(),))
        self.sp.conn.commit()

    def idValue(self) -> int:
        """
        Method that takes max id value for insertion into the letter_info table
        or returns 0 as the id value if the letter_info table is an empty table.
        """
        self.sp.cur.execute('SELECT MAX("id") FROM letter_info')
        idLett = self.sp.toConvertValidFormat(self.sp.cur.fetchone())
        if idLett == "None":
            idLett = 0
            return int(idLett)
        else:
            return int(idLett)

    def confirmation(self, person: str, date: datetime.datetime):
        """
        Method that displays a message box to get confirmation from user before sending operation.
        """
        message = "Your message will be sent to the e-mail address {} of person {} at {} time, do you confirm?\nYou cannot undo this action!".format(self.ui.emailsForSend.currentText(), person, datetime.datetime.ctime(date))
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Question)
        msgBox.setText(message)
        msgBox.setWindowTitle("Confirmation")
        msgBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
        msgBox.setEscapeButton(QMessageBox.Cancel)
        result = msgBox.exec_()
        if result == QMessageBox.Ok:
            self.addData()
            self.successful()

    def isFull(self) -> bool:
        """
        Method that checks whether the user entered a text of at least 2 characters.
        """
        if len(self.ui.title.text().replace(" ","")) >= 2:
            if len(self.ui.letter.toPlainText().replace(" ","")) >= 2:
                return True
        return False

    def isPastOrNow(self) -> bool:
        """
        Method that checks whether the time is in the past or present.
        """
        if self.ui.dateTime.dateTime().toPyDateTime() <= datetime.datetime.now():
            return True
        return False

    def noneValueError(self):
        QMessageBox.warning(self, "None value error", "You entered a null value. Try entering at least 2 characters.", QMessageBox.Ok)

    def timeError(self):
        QMessageBox.warning(self, "Time error", "You entered past or now as time. Enter a future time.", QMessageBox.Ok)
        
    def successful(self):
        QMessageBox.information(self, "Successful", "Congratulations! Completed successfully.\nThe process will start, when you close the application.", QMessageBox.Ok)
    
    def backHomePage(self):
        """
        Method that allows returning to the Home Page in the App Window.
        """
        self.ui.application.setCurrentIndex(0)
