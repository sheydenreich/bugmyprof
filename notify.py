from getpass import getpass

# get the login password for the E-Mail account. Could in principle be read from file or hard-coded in here,
# but I do not want to save my password anywhere in readable format.
password = getpass()

import socket

import smtplib
from email.message import EmailMessage
# import ssl
from time import sleep
import sys
import subprocess
import datetime

port = 465  # For SSL



def write_email(email_address,subject="",textfile="email_message.txt",
verbose=False,content=None,sender_name="",recipient_name=""):
    # Read in the email text from a file
    msg = EmailMessage()
    if content is None:
        with open(textfile) as fp:
            content = fp.read().replace("NAME1",sender_name).replace("NAME2",recipient_name)
    if(verbose):
        print("Content: ",content)
    msg.set_content(content)


    msg['From'] = 's6svheyd@uni-bonn.de'
    msg['To'] = email_address
    msg['Subject'] = subject
    with smtplib.SMTP("mail.uni-bonn.de", 587) as server:
        server.starttls()
        server.login("s6svheyd", password)
        server.send_message(msg)
    return 0

if(__name__=="__main__"):
    # try logging in to verify password
    print("Trying login...")
    with smtplib.SMTP("mail.uni-bonn.de", 587) as server:
        server.starttls()
        server.login("s6svheyd", password)
    print("... success!")
    # get current directory
    import pathlib
    working_directory = pathlib.Path().resolve()

    # get current machine
    machine = socket.gethostname()



    cmdcommand = sys.argv
    start = 1
    recipients = ["sven@astro.uni-bonn.de"]
    for i in range(1,len(cmdcommand)):
        if "@" in cmdcommand[i]:
            recipients.append(cmdcommand[i])
            start += 1
        else:
            break

    command = sys.argv[start:]

    print("Sending confirmation email to: ",recipients)
    print("Running command ",command)
    startt = datetime.datetime.now()
    p = subprocess.Popen(command)
    if(p.wait() == 0):
        endt = datetime.datetime.now()
        subject = "[AIfA Server run] Sven's call of {} on {} finished".format(sys.argv[start],machine)
        commandstr = ""
        for arg in command:
            commandstr += arg+" "
        commandstr = commandstr[:-1]
        content = """
        Execution in
        {}
        of code 
        {}
        has concluded on {}.
        Started run at {}. Finished at {}.
        Time taken: {}
        """.format(working_directory,commandstr,machine,startt,endt,endt-startt)
        for rec in recipients:
            write_email(rec,content=content,subject=subject)
    else:
        print("Something wrent wrong!")

        endt = datetime.datetime.now()
        subject = "[AIfA Server run] Your call of {} on {} did not finish properly!".format(sys.argv[1],machine)
        commandstr = ""
        for arg in command:
            commandstr += arg+" "
        commandstr = commandstr[:-1]
        content = """
        Execution in
        {}
        of code 
        {}
        has concluded on {}.
        Started run at {}. Cancelled at {}.
        Time taken: {}
        """.format(working_directory,commandstr,machine,startt,endt,endt-startt)
        write_email("sven@astro.uni-bonn.de",content=content,subject=subject)
