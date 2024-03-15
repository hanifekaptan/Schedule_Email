import psycopg2
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import QtGui
from SettingsWindow import Ui_Dialog

class Settings(QDialog):

    def __init__(self):
        super().__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.connect()
        self.begginingProccess()
        self.ui.saveB.clicked.connect(self.saveChange)
        self.ui.openAddPageB.clicked.connect(self.openInsertPage)
        self.ui.name.textChanged.connect(self.validLowChar)
        self.ui.lastname.textChanged.connect(self.validLowChar)
        self.ui.lastname.textChanged.connect(self.validLowChar)
        self.ui.addB.clicked.connect(self.control)
        self.ui.cancelFromAddB.clicked.connect(self.cancel)
        self.ui.openDelPageB.clicked.connect(self.openDelPage)
        self.ui.deleteB.clicked.connect(self.deleteEmail)
        self.ui.cancelFromDelB.clicked.connect(self.cancel)
        
    def begginingProccess(self):
        """
        Basic operations when the application is started.
        """
        self.ui.emailList.addItems(self.mails())
        self.ui.emailsForDel.addItems(self.mails())
        self.ui.defaultMail.setText(self.defaultMail())

    def mails(self) -> list:
        """
        Method that returns the current e-mail list.
        """
        self.cur.execute('SELECT "email" FROM settings_info;')
        mails = []
        [mails.append(self.toConvertValidFormat(i)) for i in self.cur.fetchall()]
        return mails
    
    def defaultMail(self) -> str:
        """
        Method that returns the current default e-mail.
        """
        self.cur.execute('SELECT "email" FROM settings_info WHERE "default_v" = true;')
        default = self.toConvertValidFormat(self.cur.fetchone())
        return default
    
    def isDefaultErr(self) -> bool:
        """
        Method that checks whether lenght of default e-mail is more or less than 1.
        """
        self.cur.execute('SELECT "email" FROM settings_info WHERE "default_v" = true;')
        default = self.cur.fetchall()
        if len(default) != 1:
            return True
        return False
    
    def autoDefault(self):
        """
        Method that assigns the first e-mail in the e-mail list as the default e-mail value.
        """
        mail = str(self.mails()[0])
        self.cur.execute('UPDATE settings_info SET "default_v" = true WHERE "email" = %s;',(mail,))
        self.conn.commit()

    def isListEmpty(self) -> bool:
        """
        Method that checks whether lenght of the mail list is less then 1.
        """
        if len(self.mails()) < 1:
            return True
        return False

    def reorganize(self):
        """
        Method that gives false to those whose default value is true.
        """
        self.cur.execute('SELECT "email" FROM settings_info WHERE "default_v" = true')
        [self.cur.execute('UPDATE settings_info SET "default_v" = false WHERE "email" = %s',(i,)) for i in self.cur.fetchall()]
        self.conn.commit()

    def saveChange(self):
        """
        Method that saves changes.
        """
        if self.ui.emailList.currentIndex != 0:
            if self.isListEmpty() == True:
                self.emptyListError()
            else:
                oldDefault = self.ui.defaultMail.text()
                newDefault = self.ui.emailList.currentText()
                self.ui.defaultMail.setText(newDefault)
                if self.isDefaultErr() == True:
                    self.reorganize()
                    self.autoDefault()
                else:
                    self.cur.execute('UPDATE settings_info SET "default_v" = false WHERE "email" = %s',(oldDefault,))########
                    self.conn.commit()
                    self.cur.execute('UPDATE settings_info SET "default_v" = true WHERE "email" = %s',(newDefault,))
                    self.conn.commit()
                self.ui.emailList.setCurrentIndex(0)
        else:
            pass

    def openInsertPage(self):
        """
        Method that opens the Add Page.
        """
        self.ui.settings.setCurrentIndex(2)
    
    def validLowChar(self):
        """
        Method that translates invalid characters in the Add Page.
        """
        transTable = str.maketrans("ığüşöçé!'^+%&/()=?_<>£#${[}]\\|*-,;`:ßæ€","igusoc"+33*" ")
        self.ui.name.setText(((self.ui.name.text().lower()).translate(transTable)).replace(" ",""))
        self.ui.lastname.setText(((self.ui.lastname.text().lower()).translate(transTable)).replace(" ",""))
        self.ui.email.setText(((self.ui.email.text().lower()).translate(transTable)).replace(" ",""))

    def control(self):
        """
        Method that checks whether the information is validly before adding a new e-mail address.
        """
        if self.isFull() == False:  # They must contain at least 2 characters
            self.noneValueError()
        elif self.isCharOk() == False:  # They must consist of valid character values
            self.charValueError()
        elif self.isFormatOk() == False:  # E-mail value must be valid format
            self.invalidValueError()
        else:
            self.addNewMail()
            self.successful()

    def isFull(self) -> bool:
        """
        Method that checks whether the user entered a text of at least 2 characters.
        """
        if len(self.ui.email.text().replace(" ","")) >= 2:
            if len(self.ui.name.text().replace(" ","")) >= 2:
                if len(self.ui.lastname.text().replace(" ","")) >= 2:
                    return True
        return False
    
    def isCharOk(self) -> bool:
        """
        Method that checks whether the data of name and lastname are in character type
        and whether the data of mail is in character or number type.
        """
        if (self.ui.name.text().replace(" ", "")).isalpha() and (self.ui.lastname.text().replace(" ", "")).isalpha():
            if ((self.ui.email.text().replace("@", "")).replace(".","")).isalnum():
                return True
        return False
    
    def isFormatOk(self) -> bool:
        """
        Method that checks whether data of mail is valid format:\n
            a. It must contain only one '@' sign\n
            b. It must not start with '.'\n
            c. It must not contain two consecutive '.'\n
            d. The lenght of the username must be at least 6 and at most 30\n
            e. It must have '.com' extension.
        """
        if "@" in self.ui.email.text():
            if self.ui.email.text().count("@") == 1:
                if self.ui.email.text()[0] != ".":
                    if ".." not in self.ui.email.text():
                        mail = list(self.ui.email.text().partition("@"))
                        if len(mail[0]) > 6 and len(mail[0]) < 30:
                            if ".com" in mail[2]:
                                return True
        return False

    def addNewMail(self):
        """
        Method that adds a new e-mail address.
        """
        self.cur.execute("INSERT INTO settings_info VALUES('{}','{}','{}','false');".format(
            self.ui.email.text(),self.ui.name.text(),self.ui.lastname.text()))
        self.conn.commit()
        self.updateCombobox()
        self.ui.email.clear(), self.ui.name.clear(), self.ui.lastname.clear()
    
    def deleteEmail(self):
        """
        Method that performs the delete operation based on the e-mail address received from the user
        If the deleted items is also the default email, it assigns a new value.
        """
        if self.ui.emailsForDel.currentIndex != 0:
            self.cur.execute('DELETE FROM settings_info WHERE "email" = %s;', (self.ui.emailsForDel.currentText(),))
            self.conn.commit()
            self.ui.deletedEmail.setText(self.ui.emailsForDel.currentText())
            self.updateCombobox()
            self.ui.emailsForDel.setCurrentIndex(0)
            if self.isListEmpty() == True:
                pass
            else:
                if self.isDefaultErr() == True:
                    self.reorganize()
                    self.autoDefault()

    def openDelPage(self):
        """
        Method that opens the Delete Page.
        """
        self.ui.settings.setCurrentIndex(1)

    def cancel(self):
        """
        Method that allows returning to the Main Page in the Settings Window.
        """
        self.ui.settings.setCurrentIndex(0)
    
    def updateCombobox(self):
        """
        Method that updates the email lists in the Settings Window after
        inserting and deleting operations.
        """
        self.ui.emailList.clear()
        self.ui.emailsForDel.clear()
        self.ui.emailList.addItem("Choose one")
        self.ui.emailsForDel.addItem("Choose one")
        self.ui.emailList.setItemIcon(0, QtGui.QIcon(":/icons/person.jpg"))
        
        self.ui.emailsForDel.setItemIcon(0, QtGui.QIcon(":/icons/person.jpg"))
        self.ui.emailList.addItems(self.mails())
        self.ui.emailsForDel.addItems(self.mails())

    def toConvertValidFormat(self, expression) -> str:
        """
        Method that converts the output we obtain with the command cur.fetchone() into the format to be used.
        """
        expression = str(expression).replace("(","").replace(")","").replace(","
            ,"").replace("'","").replace("[","").replace("]","")
        return expression

    def connect(self):
        """
        Method that connections PostgreSQL.
        """
        self.conn = None
        try:
            self.conn = psycopg2.connect(host = "localhost",
                                         database="tttf",
                                         user="postgres",
                                         password="secret")
            self.cur = self.conn.cursor()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)

    def disconnect(self):
        """
        Method that disconnections PostgreSQL.
        """
        self.conn.commit()
        self.cur.close()
        if self.conn is not None:
            self.conn.close()
                    
    def noneValueError(self):
        QMessageBox.warning(self, "None value error", "You entered a null value. Try entering at least 2 characters.", QMessageBox.Ok)
      
    def charValueError(self):
        QMessageBox.warning(self, "Character value error", "You used undefined character.", QMessageBox.Ok)
     
    def invalidValueError(self):
        QMessageBox.warning(self, "Invalid value error", "You entered an invalid e-mail adress.", QMessageBox.Ok)

    def emptyListError(self):
        QMessageBox.warning(self, "Empty list error", "No item found to list. You must enter an email address to make a transaction.", QMessageBox.Ok)

    def successful(self):
        QMessageBox.information(self, "Successful", "Congratulations! Completed successfully.", QMessageBox.Ok)
