import socket
import sys
import hmac

listenPort_a = sys.argv[1]
listenPort_c = sys.argv[2]

DNSTS1 = {}
file = open("PROJ3-DNSTS1.txt", "r")

#looping through each line to fill table info
for line in file: 
	elems = line.split()
	hostname = elems[0].lower()
	value = elems[1]+" "+elems[2]
	DNSTS1[hostname] = value
	

file.close() 

#retreiving key from file
file2 = open("PROJ3-KEY1.txt", "r")
key = file2.readline().rstrip()
file2.close()

print("TS1 KEY: "+key)

try:
	asSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("[S]: RS server socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()


server_hostname = socket.gethostname()
server_address_a = (server_hostname, int(listenPort_a))
print("ADDRESS: "+ str(server_address_a))
asSock.bind(server_address_a)
asSock.listen(1)

print("[S]: Server host name is {}".format(server_hostname))
host_ip = (socket.gethostbyname(server_hostname))
print("[S]: Server IP address is {}".format(host_ip))
asConn, addr = asSock.accept()


keepReceiving = True
while keepReceiving:
	data = asConn.recv(128)
	print("DATA: "+data)
	splitData = data.split(',')
	for line in splitData:
		if line == "finish":
			keepReceiving = False
		elif line != '':
			print(line)
			challenge = line.split(' ')[1]

			createDigest = hmac.new(key.encode("utf-8"), challenge.encode("utf-8"))
			digest = createDigest.hexdigest()
			print("KEY: "+key+" Challenge: "+challenge+" digest: "+digest)
			asConn.sendall(digest)



asConn.close()


#Receiving queries from client after authentication

try:
	clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("[S]: TS1 server socket created")
except socket.error as err:
	print('socket open error: {}\n'.format(err))
	exit()

server_hostname = socket.gethostname()
server_address_c = (server_hostname, int(listenPort_c))
print("ADDRESS: "+ str(server_address_c))
clientSock.bind(server_address_c)
clientSock.listen(1)

print("[S]: Server host name is {}".format(server_hostname))
host_ip = (socket.gethostbyname(server_hostname))
print("[S]: Server IP address is {}".format(host_ip))
clientConn, addr = clientSock.accept()

keepReceivingQueries = True

while keepReceivingQueries:
	queryData = clientConn.recv(1024)

	resolvedEntry = ""
	print("QUERY DATA: "+ queryData)
	queries = queryData.split(',')
	for hostname in queries:
		print("checking hostname "+hostname)
		resolvedEntry = ""
		if hostname == "finish":
			keepReceivingQueries = False
		elif hostname != '':
			print("hostname: "+hostname)
			if hostname in DNSTS1:
				resolvedEntry = hostname + " " + DNSTS1[hostname]
			else:
				resolvedEntry = hostname + " - Error:HOST NOT FOUND"
			clientConn.sendall(resolvedEntry)






