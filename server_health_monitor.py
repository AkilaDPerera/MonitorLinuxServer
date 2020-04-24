'''
Created on Apr 23, 2020

@author: Akila D Perera
@language: python2

analyze_server function can be used to monitor linux/ubuntu server and send a warning email in the case of reaching the server specification limits (set thresholds).
'''

import os
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send(subject, message, toEmail, fromEmail, fromEmailPassword): 
    '''
        Sending plain text emails
        Args:
            subject - (String) subject of the email
            message - (String) body of the email
            toEmail - (String) recipient's email address
            fromEmail - (String) google email address that you own with ability to access by third party applications (unsecured); https://support.google.com/accounts/answer/6010255?hl=en
            fromEmailPassword - (String) password of the google email that you own 
    '''
    try:
        msg = MIMEMultipart()
        msg['From'] = fromEmail
        msg['To'] = toEmail
        msg['Subject'] = subject
        msg.attach(MIMEText(message))

        mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        # identify ourselves to smtp gmail client
        mailserver.ehlo()
        # secure our email with tls encryption
        mailserver.starttls()
        # re-identify ourselves as an encrypted connection
        mailserver.ehlo()
        mailserver.login(fromEmail, fromEmailPassword)

        mailserver.sendmail(fromEmail, msg['To'], msg.as_string())

        mailserver.quit()
    except:
        pass

def analyze_server(CPUIdlePerThreshold, MemAvaiPerThreshold, DiskFreePerThreshold, location, isEmailWarningsOn=False, toEmail="", fromEmail="", fromEmailPassword=""):
    ''' 
        Read the server CPU, Memory, and Disk utilization values and issue warnings
        Args:
            CPUIdlePerThreshold - (int) 0 - 100; Threshold as percentage of CPU Idle
            MemAvaiPerThreshold - (int) 0 - 100; Threshold as percentage of Memory availablity
            DiskFreePerThreshold - (int) 0 - 100; Threshold as percentage of Disk free space
            location - (String) absolute location to the ServerHealth.log file (create empty file if it is not already there and give write access to it)
            isEmailWarningsOn - (bool) if False, you don't need to pass below parameters
            message - (String) body of the email
            toEmail - (String) recipient's email address
            fromEmail - (String) google email address that you own with ability to access by third party applications (unsecured); https://support.google.com/accounts/answer/6010255?hl=en
            fromEmailPassword - (String) password of the google email that you own 
    '''

    data = os.popen('free -m').readlines()
    title = data[0].split()
    mem = data[1].split()
    swap = data[2].split()

    totalMem = "Total RAM: %sMB"%(mem[1])
    availableMem = "Avaliable RAM: %sMB"%(mem[6])
    availablePercentageMemVal = int(mem[6])*100/int(mem[1])
    availablePercentageMem = "Available Percentage: %d"%(availablePercentageMemVal) + "%"

    totalSwap = "Total SWAP: %sMB"%(swap[1])
    freeSwap = "Free SWAP: %sMB"%(swap[3])
    freePercentageSwapVal = int(swap[3])*100/int(swap[1])
    freePercentageSwap = "Free Percentage: %d"%(freePercentageSwapVal) + "%"

    data = os.popen('df -h').readlines()
    root = data[1].split()
    freeSpaceVal = 100 - int(root[4][:-1])
    freeSpace = "Free Space: %s"%(freeSpaceVal)

    data = os.popen('iostat').readlines()
    cpu = data[3].split()
    idle_cpu_val = float(cpu[-1])
    idleCPU = "IDLE CPU: %.2f"%(idle_cpu_val) + "%"

    output = str(datetime.datetime.now()) + " - CPU: %s | MEM: %s , %s , %s | SWAP: %s , %s , %s | SSD: %s\n"%(idleCPU, availablePercentageMem, totalMem, availableMem, freePercentageSwap, totalSwap, freeSwap, freeSpace)

    try:
        with open(location+"ServerHealth.log", "a") as f:
            if availablePercentageMemVal<MemAvaiPerThreshold or freeSpaceVal<DiskFreePerThreshold or idle_cpu_val<CPUIdlePerThreshold:
                f.write("WARNING: "+output)
                if isEmailWarningsOn:
                    send("PRIMARY SERVER HEALTH", "WARNING: "+output, toEmail, fromEmail, fromEmailPassword)
            else: 
                f.write("\t\t\t"+output)
    except:
        print("Please create an empty file as %s, if the file does not exist."%(location+"ServerHealth.log", ))
