#!/usr/bin/env python

import sys

# The length of the length string
LEN_LEN = 100

########################################################################
# Sends all data 
# @param sock - the socket to send the data over
# @param data - the actual data to send
########################################################################
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
	
########################################################################
# Sends the size 
# @param sock - the socket to send it over
# @param size - the size to send
########################################################################
def sendSize(sock, size):	
	# Convert the size into string
	strSize = str(size) 	
	# Padd the size with leading 0's
	while len(strSize) < LEN_LEN:
		strSize = "0" + strSize	
	# Send the size
	sendData(sock, strSize)

########################################################################
# getFileInfo - gets information about a file
# @param filepath - the relative path to the file
# #return - Tuple - (file pointer, file size, file name)	
#         - None if invalid file path
########################################################################
def getFileInfo(filepath):
    try:
        fp = open(path, 'rb')
        size = os.path.getsize(path)
        p, filename = os.path.split(path)
        return (fp, size, filename)
    except:
        return None
    

def main(server, port):
    	
    #Host to connect to
    host = sys.argv[1]

    #Port to send to
    port = int(sys.argv[2])    
        
    #connect to host - command socket
    conSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        #convert host input to ip    
        addrinfo = socket.getaddrinfo(host, port)
        host = addrinfo[0][4][0]        
        conSocket.connect((host,port))
    except:
        print "Error connecting to host"
        exit(0)
    
    #listen for input commands
    while(True):
        cmd = raw_input("ftp> ")
        
        if cmd[0:3] == 'get':
            pass
        elif cmd[0:3] == 'put':
            pass
        elif cmd[0:2] == 'ls':
            pass
        elif cmd[0:3] == 'bye' or cmd[0:4] == 'exit':
            print 'bye'
            exit(0)
        else:
            print "Unknown command"
    
    
    
    return
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: ", sys.argv[0], " <Server IP> <Server Port>"
        exit(0)
    main(sys.argv[1], sys.argv[2])




