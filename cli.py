#!/usr/bin/env python

import sys

# The length of the length string
LEN_LEN = 100

# ------------------------------------------------
# Sends all data 
# @param sock - the socket to send the data over
# @param data - the actual data to send
# -------------------------------------------------
def sendData(sock, data):
	
	# The total number of bytes sent in one shot
	numSent = 0
	
	# The cumulative number of bytes sent
	totalNumSent = 0
	
	# Send all the data
	while totalNumSent < len(data):
		
		# Send as much as you can
		numSent = sock.send(data[totalNumSent:])
		
		# Update how many bytes were sent thus far
		totalNumSent += numSent
	
	return totalNumSent
	
# -----------------------------------------------------
# Sends the size 
# @param sock - the socket to send it over
# @param size - the size to send
# ------------------------------------------------------
def sendSize(sock, size):
	
	# Convert the size into string
	strSize = str(size) 
	
	# Padd the size with leading 0's
	while len(strSize) < LEN_LEN:
		strSize = "0" + strSize;
	
	# Send the size
	sendData(sock, strSize)
	


def main(server, port):
    
    return
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: ", sys.argv[0], " <Server IP> <Server Port>"
        exit(0)
    main(sys.argv[1], sys.argv[2])




