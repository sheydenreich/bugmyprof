from getpass import getpass

import smtplib
from email.message import EmailMessage

from datetime import time,timedelta,datetime
import sys


class EmailHandler():
    """
    This class handles the sending of email messages, including storing the login information
    and the email address of the sender.
    """
    def __init__(self,email_username,email_domain="smtp.gmail.com",port=587,password=None,verbose = False):
        if password is None:
            self.password = getpass()
        else:
            self.password = password
        self.username = email_username
        self.domain = email_domain
        self.verbose = verbose
        self.port=port
        if(self.verbose):
            print("Trying login...")
        with smtplib.SMTP(self.domain, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
        if(self.verbose):
            print("... success!")

    def write_email(self,email_address,content,from_address=None,
                    subject=""):
        """
        This function sends an email to the specified email address with the specified content.
        Input:
            email_address: address to send the mail [string]
            content: content of the email [string]
            from_address: address to send the mail from [string]
            subject: subject of the email [string]
        Output:
            0 if successful
        """
        msg = EmailMessage()
        msg.set_content(content)

        if from_address is None:
            msg['From'] = self.username+"@"+self.domain
        else:
            msg['From'] = from_address
        msg['To'] = email_address
        msg['Subject'] = subject
        with smtplib.SMTP(self.domain, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
        return 0
    
    def read_content_from_textfile(self,textfile,sender_name,recipient_name):
        with open(textfile) as fp:
            content = fp.read().replace("YOURNAME",sender_name).replace("RECIPIENTNAME",recipient_name)
        return content

eh = EmailHandler("svenheydenreich","smtp.gmail.com",verbose=True)
# eh.write_email("sheydenr@ucsc.edu",subject="Test",content="TEST")