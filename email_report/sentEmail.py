import smtplib
import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime as dt

class EmailConfig():

    "The main functionality of this class is to sent daily status report in table format to respective email Id"

    def __init__(self):
        pass

    def sent_email(self, SUBJECT, BODY, TO, FROM):

        """With this function we send out our email"""

        # Create message container - the correct MIME type is multipart/alternative here!
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = SUBJECT
        MESSAGE['To'] = TO
        MESSAGE['From'] = FROM

        # Record the MIME type text/html.
        HTML_BODY = MIMEText(BODY, 'html')
        MESSAGE.attach(HTML_BODY)
        print "Enter password for ",FROM
        password = getpass.getpass()
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(FROM, password)
            server.sendmail(FROM, [TO], MESSAGE.as_string())
            server.quit()

            print 'Email sent!'
        except:
            print 'Something went wrong...'

    def create_template(self,opt):
        """
        :Description:
            - The primary function of this method is to create template in html format.

        :Parameter:
            - opt - It accept list

        :Example: ''create_template('['Topic','Contents']')''

        :Return: String
        """
        lst = ['Topics', 'Contents', 'Start Date', 'End Date', 'Progress', 'Confidence Level', 'Team Member','Comments']
        self.strTable = "<html><body>Hi,</br></br><header><b>Daily Status Report : "+str(dt.now())+ \
                        "</b></Header><table border=1 cellpadding=10 cellspacing=0><tr bgcolor='#A6C4AA'>"

        for item in lst:
            str_row = "<td>" + str(item) + "</td>"
            self.strTable = self.strTable + str_row
            if item == lst[-1]:
                self.strTable = self.strTable + "</tr><tr>"

        for item1 in opt:
            str_row = "<td>" + str(item1) + "</td>"
            self.strTable = self.strTable + str_row

        strTable = self.strTable + "</tr></table></body></html>"
        return strTable

    def create_template_inprogress(self,opt):
        """
        :Description:
            - The primary function of this method is to create template in html format for
            data in progress.

        :Parameter:
            - opt - It accept list

        :Example: ''create_template('['Topic','Contents']')''

        :Return: String
        """
        lst = ['Topics', 'Contents', 'Start Date', 'End Date', 'Progress', 'Confidence Level', 'Team Member',
               'Comments']
        self.strTable = "<html><body>Hi,</br></br><header><b>Status Report For Pending Work: " + str(dt.now()) + \
                        "</b></Header><table border=1 cellpadding=10 cellspacing=0><tr bgcolor='#A6C4AA'>"

        for item in lst:
            str_row = "<td>" + str(item) + "</td>"
            self.strTable = self.strTable + str_row
            if item == lst[-1]:
                self.strTable = self.strTable + "</tr>"

        for items in opt:
            self.strTable = self.strTable + "<tr>"
            for item in items:
                str_row = "<td>" + str(item) + "</td>"
                self.strTable = self.strTable + str_row
            self.strTable = self.strTable + "</tr>"

        strTable = self.strTable + "</tr></table></body></html>"
        return strTable