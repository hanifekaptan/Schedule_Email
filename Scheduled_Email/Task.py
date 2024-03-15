import psycopg2
import smtplib
import time
import json
from datetime import datetime
from email.message import EmailMessage

class Task:
    def __init__(self):
        self.connect()
        with open("emailInfo.json") as file:
            self.eInfo = json.load(file)

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
            self.conn = self.conn.close()

    def send(self, dt):
        """
        Method that makes the sending operations and deletes sent letter.
        """
        self.sendWithSMTP()
        self.cur.execute('DELETE FROM letter_info WHERE "datetime" = %s;', (dt,))
        self.conn.commit()
        self.disconnect()
 
    def contentInfo(self) -> list:
        """
        Method that returns info containing Email, Title and Message as a list.
        """
        self.cur.execute('SELECT "email","title","message" FROM letter_info ORDER BY "datetime" LIMIT 1')
        info = list(self.cur.fetchone()[0:3])
        return info

    def content(self) -> EmailMessage:
        """
        Method that prepares e-mail content.
        """
        info = self.contentInfo()
        mail = EmailMessage()
        mail["Subject"] = info[1]
        mail["From"] = str(self.eInfo["emailAddress"])
        mail["To"] = info[0]
        mail.set_content(info[2])
        return mail

    def sendWithSMTP(self):
        """
        Method that sends the e-mail with SMTP.
        """
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(user=self.eInfo["emailAddress"], password=self.eInfo["password"])
            smtp.send_message(from_addr=self.eInfo["emailAddress"], to_addrs=self.contentInfo()[0], msg=self.content())

    def proccess(self):
        """
        Method that checks whether the target date is today and directs you to work if it is today.
        """
        if self.isTableEmpty() == False:
            self.cur.execute('SELECT "datetime" FROM letter_info ORDER BY "datetime" ASC LIMIT 1;')
            target = self.cur.fetchone()
            dt = datetime.fromtimestamp(time.mktime(datetime.timetuple(target[0])))
            if dt.date() == datetime.today().date():
                if dt.hour == datetime.now().hour and dt.minute == datetime.now().minute:
                    self.send(target)
        else:
            pass

    def isTableEmpty(self) -> bool:
        """
        Method that checks whether the letter_info table is null.
        """
        if self.isConnNone() == True:
            self.connect()
        self.cur.execute('SELECT "id" FROM letter_info')
        number = []
        [number.append(list(i)) for i in self.cur.fetchall()]
        if len(number) < 1:
            return True
        return False

    def isConnNone(self) -> bool:
        """
        Method that checks whether the conn is connect.
        """
        if self.conn == None:
            return True
        else:
            return False
