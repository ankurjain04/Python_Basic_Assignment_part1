"""
Write a python code to accept input for following format of daily status report from python
terminal. Write this information to a delimiter separated file. New information should be
appended at the end of the file. FilePath, FileName, Delimiter, Date Format to display:
should be configurable through config file. Input received should also be emailed to
pre-configured email list
"""

import configparser
import re
import os
from datetime import datetime as dt
from email_report.sentEmail import EmailConfig

class DailyStatus:
    """
     Functionality of this class is to take daily status report from user , write it to output file
     and sent report mail to respective receipent mention in config file.
    """
    def __init__(self):

        config_path =  '/configfiles/config.ini'
        abs_path = os.getcwd() + config_path
        configParser = configparser.RawConfigParser()
        configParser.read(abs_path)
        self.file_path = configParser.get('env_config', 'filepath')
        self.file_name = configParser.get('env_config', 'filename')
        self.delimiter = configParser.get('env_config', 'delimeter')
        self.date_format = configParser.get('env_config', 'dateformat')
        self.comment_len = configParser.get('env_config', 'comment_length')
        self.from_emailid = configParser.get('email_config', 'from_emailid')
        self.to_emailid = configParser.get('email_config', 'to_emailid')
        self.email_subject = configParser.get('email_config', 'email_subject')

        self.input_contents = ['Topics','Contents','Start Date','End Date','Progress','Confidence Level','Team Member','Comments']
        self.output = []

    def user_inputs(self):
        """
        :Description:
            - The primary function of this method is to take the input from user.

        :Parameter: None

        :Example: None

        :Return: None
        """
        for item in self.input_contents:
            usrip = raw_input("\nEnter data for %s"%item + ": \n" )
            self.validate_inputs(item,usrip)

    def validate_anum_special_char(self, inputs, length='255'):
        """
        :Description:
            - The primary function of this method is to validate alphanumeric values
            and some special characters(!@#$%^&*()).

        :Parameter:
            - inputs - Accepts inputs.
            - length - It defines the length of the string and by default its value is 255.

        :Example: ''validate_anum_special_char('Python',300)''

        :Return: Bool
        """
        valid = re.search('^[\w.!@#$%^&*()\s]{1,' + length + '}$', inputs)

        if valid and self.delimiter not in inputs:
            self.output.append(inputs)
            return True
        else:
            print "You have entered wrong data"
            print "Please enter correct data which contains Alpha numeric and " \
                  "special character of lenght upto %s character and not contains this character (%s)"%(length,self.delimiter)

            self.validate_anum_special_char(raw_input("\nPlease enter valid data : \n"))

    def validate_team_member(self,inputs,length='100'):
        """
        :Description:
            - The primary function of this method is to validate alphanumeric values.

        :Parameter:
            - inputs - Accepts inputs.
            - length - It defines the length of the string and by default its value is 100.

        :Example: ''validate_team_member('Python',300)''

        :Return: Bool
        """
        valid = re.search('^[\w.\s]{1,' + length + '}$', inputs)

        if valid and self.delimiter not in inputs:
            self.output.append(inputs)
            return True
        else:
            print "You have entered wrong data"
            print "Please enter correct data which contains Alpha numeric character of lenght upto %s character " \
                  "and not contains special charater and this character (%s)"%(length,self.delimiter)

            self.validate_team_member(raw_input("\nPlease enter valid data : \n"))

    def validate_start_date(self,inputs):
        """
        :Description:
            - The primary function of this method is to validate date and
            check it should not take future date.

        :Parameter:
            - inputs - Accepts inputs.

        :Example: ''validate_start_date('30/10/2018')''

        :Return: Bool
        """
        try:
            entered_date = (dt.strptime(inputs, str(self.date_format))).strftime(str(self.date_format))
            cur_date = dt.now().strftime(self.date_format)

            if cmp(cur_date, entered_date) >= 0:
                self.output.append(entered_date)
                return True
            else:
                print "You have entered wrong date"
                print "Please enter date in format %s" % (self.date_format)
                self.validate_start_date(raw_input("\nPlease enter valid data : \n"))
        except:
            print "Enetred Date is not in format of %s please re-enter again either giving full year or " \
                  "only last two digits of year" % (self.date_format)
            self.validate_start_date(raw_input("\nPlease enter valid data : \n"))

    def validate_end_date(self,inputs):
        """
        :Description:
            - The primary function of this method is to validate date and
            check it should not take future date.

        :Parameter:
            - inputs - Accepts inputs.

        :Example: ''validate_end_date('31/10/2018')''

        :Return: Bool
        """
        try:
            entered_date = (dt.strptime(inputs, str(self.date_format))).strftime(str(self.date_format))
            cur_date = dt.now().strftime(self.date_format)

            if (cmp(cur_date, entered_date) >= 0) and (cmp(entered_date,self.output[-1]) >= 0) :
                self.output.append(entered_date)
                return True
            else:
                print "You have entered wrong date"
                print "Please enter date in format %s or end date should be " \
                      "equal or greater than start date %s" % (self.date_format,self.output[-1])
                self.validate_start_date(raw_input("\nPlease enter valid data : \n"))
        except:
            print "Enetred Date is not in format of %s please re-enter again either giving full year or " \
                  "only last two digits of year" % (self.date_format)
            self.validate_start_date(raw_input("\nPlease enter valid data : \n"))
        pass

    def validate_inputs(self, content, inputs):

        if content == 'Topics' or content == 'Contents':
            return self.validate_anum_special_char(inputs)

        elif content == 'Comments':
            return self.validate_anum_special_char(inputs,length=self.comment_len)

        elif content == 'Team Member':
            return self.validate_team_member(inputs)

        elif content == 'Progress':
            if inputs.title() == 'Completed' or inputs.title() == 'Inprogress':
                self.output.append(inputs.title())
                return True
            else:
                print "You have entered wrong data"
                print "Please enter progress values as Completed or Inprogress"
                self.validate_inputs(content,raw_input("\nPlease enter valid data : \n"))

        elif content == 'Confidence Level':
            conf_lvl = ['High','Medium','Low']
            if inputs.title() in conf_lvl:
                self.output.append(inputs.title())
                return True
            else:
                print "You have entered wrong data"
                print "Please enter Confidence Level as High,Low or Medium"
                self.validate_inputs(content, raw_input("\nPlease enter valid data : \n"))

        elif content == 'Start Date':
            return self.validate_start_date(inputs)

        elif content == 'End Date':
            return self.validate_end_date(inputs)

        else:
            print "Invalid Input"

    def write_to_file(self):
        """
        :Description:
            - The primary function of this method is to write contents to the file

        :Parameter: None

        :Example:

        :Return: None
        """
        with open(self.file_path+self.file_name,'a') as fp:
            opt = self.output
            for ele in range(len(opt)-1):
                fp.write(opt[ele] + self.delimiter)

            fp.write(opt[-1]+"\n")

    def parse_output_list(self):
        """
        :Description:
            - The primary function of this method is to parse output list

        :Parameter: None

        :Example:

        :Return: List
        """
        return self.output

if __name__ == '__main__' :
    cd = DailyStatus()
    cd.user_inputs()
    cd.write_to_file()
    EC = EmailConfig()
    lst = cd.parse_output_list()
    body = EC.create_template(lst)
    sub = cd.email_subject
    to = cd.to_emailid
    From = cd.from_emailid
    EC.sent_email(sub, body, to, From)