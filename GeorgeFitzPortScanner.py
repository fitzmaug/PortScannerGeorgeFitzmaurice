#!/usr/bin/env python
#
# George Fitzmaurice port scanner
#
# This python program will scan ports 1-1025 and report if they are open or closed.  Output is shown on the screen
# and also in the output file named GeorgeFitz_outfile.txt.  The output file is overwritten on each subsequent run.
#
# User enters a hostname and that host is scanned
#


import socket
import subprocess
from datetime import datetime

#
# Create a function to format date time in the way we want it displayed
# m/d/y H:M:S
#


def formatDateTime(dateTime):
    return dateTime.strftime("%m/%d/%Y %H:%M:%S")


#
# function to print and write to an output file
#


def printAndWriteFile(fileToUse, stringToOutput):
    print(stringToOutput)
    fileToUse.write(stringToOutput+"\n")
#
# Check that a given host IP responds to ping
#


def checkHostPing(IP):

    # Determine system type - Windows needs ping -n and mac/linux need ping -n
    try:
        output = subprocess.check_output(
            "ping -{} 1 {}".format('n' if platform.system().lower() == "windows" else 'c', IP), shell=True)
    except Exception as e:
        return False

    return True


#
# Function to connect to a port on a given host and return if the port is open or closed.
#


def checkPort(hostName, portNum):
    s = socket.socket()
    s.settimeout(5)  # setting a 5 sec timeout so this completes faster
    try:
        s.connect((hostName, portNum))
    except Exception:
        return False
    else:
        return True


#
################################
# MAIN Program
################################


#
# Open the output file
#


outFile = open("GeorgeFitz_outfile.txt", "w")


#
# Ask for Host to scan
#


serverToScan = input("Enter a host to scan : ")

#
# if user does not enter a server name exit
#

if serverToScan.isspace() or serverToScan == "":
    printAndWriteFile(outFile, "You entered a blank server name, exiting...")
    outFile.close()
    exit()


#
# initialize serverToScanIP to avoid warning.
#


serverToScanIP = ""

#
# If the server name is not blank lets see if it is good or not
#


try:
    serverToScanIP = socket.gethostbyname(serverToScan)
except Exception:
    printAndWriteFile(outFile, "The host named: " + serverToScan + " could not be found, exiting...")
    outFile.close()
    exit()
#
# Now we have a resolved IP.  Check that the IP is responding.
#
if not checkHostPing(serverToScanIP):
    printAndWriteFile(outFile, "Host IP : " + serverToScanIP + " is not responding.  exiting...")
    exit()
#
# We have a resolved and responding IP - Lets scan.
#
#
# Print and write to outfile a banner with information on which host we are about to scan
#
printAndWriteFile(outFile, "=" * 60)
printAndWriteFile(outFile, "Please wait, scanning remote host: " + serverToScan + " IP: " + serverToScanIP)
printAndWriteFile(outFile, "=" * 60)
#
# Get Scan Start Time and write it to outFile and print it out
#
startTime = datetime.now()
printAndWriteFile(outFile, "=" * 60)
printAndWriteFile(outFile, "Scan Start time: " + formatDateTime(startTime))
printAndWriteFile(outFile, "=" * 60)
#
# Do the Scan - go from 1 to 1026 to insure we get port 1025
#
for port in range(1, 1026):
    portOpen = checkPort(serverToScanIP, port)
    if portOpen:
        printAndWriteFile(outFile, "Port: " + str(port) + "  Is Open")
    else:
        printAndWriteFile(outFile, "Port: " + str(port) + "  Is Closed")

#
# Get End Scan Time
#
endTime = datetime.now()
#
# Calculate elapsed time
#
elapsedTime = endTime - startTime

#
# Print and write to outFile banner with end time and elapsed time
#
printAndWriteFile(outFile, "=" * 60)
printAndWriteFile(outFile, "Scanning Complete at : " + formatDateTime(endTime) + "\nElapsed Scan Time: " +
                  str(elapsedTime))

printAndWriteFile(outFile, "=" * 60)
#
# Close the output file
#
outFile.close()
