import sys
import os
import shutil
from datetime import datetime
import pathlib
import backupcfg
import smtplib

"""
Script Title: Back up Program
Author: Zoe McDermott
author email: *****@company.com
Script version: v2
Description: This script checks if the relevant file or folder exists, and then backs it up, before logging the outcome into backup.log.
If there are any errors, the error and type is written to the terminal, and an elert is sent out in email form.

"""
source_file = False
dest_folder = False

"""

Sending an alert through email:

"""

smtp = {"sender": "",    # elasticemail.com verified sender
        "recipient": "", # elasticemail.com verified recipient
        "server": "in-v3.mailjet.com",      # elasticemail.com SMTP server
        "port": 587,                        # elasticemail.com SMTP port
        "user": "user",      # elasticemail.com user
        "password": "password"}    # elasticemail.com password

# append all error messages to email and send
def send_email(message):

    email = 'To: ' + smtp["recipient"] + '\n' + 'From: ' + smtp["sender"] + '\n' + 'Subject: Backup Error\n\n' + message + '\n'

    # connect to email server and send email
    try:
        smtp_server = smtplib.SMTP(smtp["server"], smtp["port"])
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.ehlo()
        smtp_server.login(smtp["user"], smtp["password"])
        smtp_server.sendmail(smtp["sender"], smtp["recipient"], email)
        smtp_server.close()
    except Exception as e:
       print(f"An error occurred: {e}")
       print(f"Type of error: {type(e)}")
      
"""
Adding the Successes and Fails to backup.log:

"""
        
def add_to_log_success():
    try:
        file = open(backupcfg.backup_log, "a")
        
        file.write(sys.argv[-1] + ": SUCCESS.\n")
        
        file.close()
    except Exception as e:
       print(f"An error occurred: {e}")
       print(f"Type of error: {type(e)}")
       send_email(e)

def add_to_log_failed(error):
    try:
        file = open(backupcfg.backup_log, "a")
        
        file.write(sys.argv[-1] + f": FAIL. Erorr: {error}\n")
        
        file.close()
    except Exception as e:
       print(f"An error occurred: {e}")
       print(f"Type of error: {type(e)}")
       send_email(e)
       
"""
Copying the Files or Folders

"""

def copy_file_folder(src_file_dir):
    try:
        dateTimeStamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        
        srcLoc = src_file_dir # change this srcLoc = srcDir to test copying a directory
        srcPath = pathlib.PurePath(srcLoc)
        
        dstLoc = backupcfg.dest_folder + "/" + os.path.splitext(srcPath.name)[0] + "-" + dateTimeStamp + ".py"
        
        if pathlib.Path(srcLoc).is_dir():
            shutil.copytree(srcLoc, dstLoc, dirs_exist_ok=True)
            print('Backup Status: FAILED')
        else:
            shutil.copy2(srcLoc, dstLoc)
            print('Backup Status: SUCCESS')
            add_to_log_success()
            
    except Exception as e:
       print(f"An error occurred: {e}")
       print(f"Type of error: {type(e)}")
       add_to_log_failed(e)
       send_email(e)
       
"""
Checking to make sure the file and directory exists:

"""

def does_file_exist(file_exists):
    try:
        if os.path.exists(file_exists):
            copy_file_folder(file_exists)
        else:
            add_to_log_failed('File or Directiory Unknown')
            send_email('File or Directiory Unknown')
            print('Error: This file does not exist')
            
            
    except Exception as e:
       print(f"An error occurred: {e}")
       print(f"Type of error: {type(e)}")
       send_email(e)
       add_to_log_failed(e)
       
def does_dest_dir_exist(dest_dir_exists):
    try:
        jobnumber = sys.argv[1]
        if(jobnumber == 'job1' or jobnumber=='job2' or jobnumber=='job3'):
            if os.path.exists(dest_dir_exists):
                does_file_exist(backupcfg.source_file)
            else:
                add_to_log_failed('File or Directiory Unknown')
                send_email('File or Directiory Unknown')
                print('Error: This folder does not exist')
        else:
            add_to_log_failed('Job Number is unknown')
            send_email('Job Number is unknown')
            print('Error: Job Number is unknown')
            
            
    except Exception as e:
       print(f"An error occurred: {e}")
       print(f"Type of error: {type(e)}")
       send_email(e)
       add_to_log_failed(e)
       
"""
What the computer runs:

"""
        
if __name__ == "__main__":
    does_dest_dir_exist(backupcfg.dest_folder)
