#!/usr/bin/env python

import sys
import socket

# The length of the length string for sending files
LEN_LEN = 100

# The length of a command string
CMD_LEN = 100

#######               Command String Info            ###################
# [0-4 port number]:[6-8 command]:[10-99 cmd arg (filename)] 
# port number will be padded with 0's infront of it if len < 5
# ls command will be padded with a space after it 
# cmd arg will be padded with $'s after the text
########################################################################


########################################################################
# getCmdStr - build the command string to send
# @param - int - port - the port for the server to listen on
# @param - str - cmd - the command that was executed
# @param - str - arg - the file name or blank if ls command
# @return - str- the resulting string to send
########################################################################
def getCmdStr(port, cmd, arg=""):
    strPort = str(port)
    while len(strPort) < 5:
        strPort = "0" + strPort
    if cmd == "ls":
        cmd = "ls "
    while len(arg) < 90:
        arg = arg + "$"
        
    result = strPort + ":" + cmd + ":" + arg

    return result


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


########################################################################
# openDataSocket - gets information about a file
# @param port - Optional - the port to listen on
#             - Default = 0, gets an emphirical port
# #return - Tuple - (socket object, port)	
#         - None if invalid file path
########################################################################
def openDataSocket(port=0):
    try:
        listSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listSocket.bind(('',port))
        addr = listSocket.getsockname()
        port = addr[1]
        return (listSocket, port)
    except:
        return None


########################################################################
# Receive data
# Receives the specified amount of data
# @param sock - the socket to receive the data from
# @param size - how much to receive
# @return - the received data
########################################################################
def recvData(sock, size):
	# The buffer to store the data
    data = ""

	# Keep receiving until all is received
    while size > len(data):

		# Receive as much as you can
        data += sock.recv(size - len(data))

	# Return the received data
    return data


########################################################################
# Recieves the size
# @param sock - the socket over which to receive the size
# @return - the received size
########################################################################
def recvSize(sock):
    # Get the string size
    strSize = recvData(sock, LEN_LEN)

    # Conver the size to an integer and return
    try:
        return int(strSize)
    except:
        return None


########################################################################
#                               Main                                   # 
########################################################################
def main(server, port):  
        
    #connect to host - command socket
    cmdSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        #convert host input to ip
        addrinfo = socket.getaddrinfo(server, port)
        host = addrinfo[0][4][0]  
        cmdSocket.connect((host,port))
    except:
        print "Error connecting to host"
        exit(0)
    
    #listen for input commands
    while(True):
        cmd = raw_input("ftp> ")

        if cmd[0:2] == 'ls':
            #init objects
            
            datasock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            datasock.bind(('',0))
            addr = datasock.getsockname()
            dataport = addr[1]
            datasock.listen(1)
            
            strcmd = getCmdStr(dataport, 'ls')
            #send the command
            sendData(cmdSocket, strcmd)  
            
            #listen for reply          
            client, address = datasock.accept()
            
            #get return data size
            datalen = recvSize(client)
            
            # The size of the chunk
            chunkSize = 100            
            # The number of bytes to receive right now
            numToRecv = 0            
            # The total number of bytes received
            totalNumRecv = 0            
            #string to hold entire list of file names returned
            strfilelist = ""
            
            while totalNumRecv < datalen:
                # By default receive chunkSize bytes
                numToRecv = chunkSize
                # Is this the last chunk?
                if datalen - totalNumRecv < chunkSize:
                    numToRecv = datalen - totalNumRecv
                # Receive the amount of data
                data = recvData(client, numToRecv)
                # Save the data
                strfilelist += data              
                # Update the total number of bytes received
                totalNumRecv += len(data)
            
            #convert string to a list
            lstFiles = strfilelist.replace("[","").replace("]","").replace("'","").replace(" ","").split(",")
            
            #print the list
            for fn in lstFiles:
                print fn
                  
        elif cmd[0:3] == 'get':
            #init objects
            datasock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            datasock.bind(('',0))
            addr = datasock.getsockname()
            dataport = addr[1]
            datasock.listen(1)

            # Get the file name the user specified.
            filename = cmd[4:]

            # Tell the server to send the file.
            strcmd = getCmdStr(dataport, 'get', filename)
            sendData(cmdSocket, strcmd)

            #listen for reply          
            client, address = datasock.accept()

            # Receive the size of the file from the server.
            fileSize = recvSize(client)
            
            if fileSize:
                # Since we know the filename, open the file.
                file = open(filename, 'w')

                chunkSize   = 100
                bytesRecvd    = 0
                while (bytesRecvd < fileSize):
                    # By default receive chunkSize bytes
                    numToRecv = chunkSize

                    # Is this the last chunk?
                    if fileSize - bytesRecvd < chunkSize:
                        numToRecv = fileSize - bytesRecvd
                    # Receive the amount of data
                    data = recvData(client, numToRecv)

                    # Save the data
                    file.write(data)

                    # Update the total number of bytes received
                    bytesRecvd += len(data)

                # Transfer complete, close the file.
                file.close()

                # Show the user the file name and file size.
                print filename + ', ' + str(bytesRecvd) + ' bytes'
            else:
                print "File does not exist, try again."

        elif cmd[0:3] == 'put':
            filename = cmd[4:]
            file=open(filename)
            if not file:
                print "Please enter a valid filname"
            else:
                datasock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print "datasock created"
                addr = datasock.getsockname()
                dataport = addr[1]
                
                strcmd = getCmdStr(dataport, 'put', filename)
                sendData(cmdSocket, strcmd)
                
                datasock.connect((host,dataport))
                print "connected"
                
                print sys.getsizeof(file)
                sendSize(datasock,os.stat(filename).st_size)
                print "sent size"
                sendData(datasock, file.read())
                print "send data"
            
        elif cmd[0:4] == 'quit':
            cmdSocket.close()
            print 'ftp> Closing connection, Bye'
            exit(0)
        else:
            print "Error: Unknown command"

    return


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: ", sys.argv[0], " <Server Host> <Server Port>"
        exit(0)
    main(sys.argv[1], int(sys.argv[2]))
