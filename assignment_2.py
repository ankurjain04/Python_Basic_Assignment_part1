"""
Write a python script which will read a delimiter separated file whenever executed and will collect the records which
are 'In-Progress' past the mentioned 'End-Date'. Email should be sent to pre-configured email list in format as given
above, in html format.From Email details to be used to send mail using SMTP should be configurable in
configuration file.In case no records are found then terminal should display message No Delayed Tasks
found.It should not send email in case of no records found.
"""

import os
import configparser
from datetime import datetime as dt
from email_report.sentEmail import EmailConfig

class DataInProgress:
    """
     Functionality of this class is to read data from File which are In-progress and past End Date,
     and sent report through mail.
    """

    def __init__(self):

        config_path = '/configfiles/config.ini'
        abs_path = os.getcwd() + config_path
        configParser = configparser.RawConfigParser()
        configParser.read(abs_path)
        self.file_path = configParser.get('env_config', 'filepath')
        self.file_name = configParser.get('env_config', 'filename')
        self.delimiter = configParser.get('env_config', 'delimeter')
        self.date_format = configParser.get('env_config', 'dateformat')
        self.from_emailid = configParser.get('email_config', 'from_emailid')
        self.to_emailid_inprogress = configParser.get('email_config', 'to_emailid_inprogress')
        self.email_subject = configParser.get('email_config', 'email_subject')
        self.email_subject_pending = configParser.get('email_config', 'email_subject_pending')

    def read_data_inprogress(self):
        """
        :Description:
            - The primary function of this method is to read data from file which are in progress
            and whose end date is passed current date.

        :Parameter: None

        :Example:

        :Return: List
        """
        with open('report', 'r') as fp:
            obj = fp.readlines()
            opt = []
            for item in obj:
                lst = item.split(',')
                cur_date = dt.strptime(dt.now().strftime(self.date_format),self.date_format)
                end_date = dt.strptime(lst[3],self.date_format)

                if lst[4] == 'Inprogress':
                    if cur_date > end_date:
                        print "Delayed Task : ",lst
                        opt.append(lst)

            return opt

if __name__ == '__main__':

    DP = DataInProgress()
    lst = DP.read_data_inprogress()
    if len(lst) != 0:
        EC = EmailConfig()
        body = EC.create_template_inprogress(lst)
        sub = DP.email_subject_pending
        From = DP.from_emailid
        to = DP.to_emailid_inprogress
        email_list = to.split(',')
        for email in email_list:
            To = email
            EC.sent_email(sub, body, To, From)
    else:
        print "No Delayed Tasks Found"