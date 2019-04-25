import socket
import sys
import hmac

listenPort = sys.argv[1]
ts1Hostname = sys.argv[2]
ts1ListenPort_a = sys.argv[3]
ts2Hostname = sys.argv[4]
ts2ListenPort_a = sys.argv[5]

sendBack = []

try:
	ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("[S]: AS server socket created")
except socket.error as err:
    print('socket open error: {}\n'.format(err))
    exit()


server_hostname = socket.gethostname()

server_address = (server_hostname, int(listenPort))
print("ADDRESS: "+ str(server_address))
ss.bind(server_address)
ss.listen(1)

print("[S]: Server host name is {}".format(server_hostname))
host_ip = (socket.gethostbyname(server_hostname))
print("[S]: Server IP address is {}".format(host_ip))
clientConn, addr = ss.accept()
print('Connected by', addr)

cdPairs = []
keepReceiving = True
while keepReceiving:
	data = clientConn.recv(128)
	print("Challenge DATA: "+data)
	splitData = data.split(',')
	for line in splitData:
		if line == "finish":
			keepReceiving = False
		elif line != '':
			cdPairs.append(line.rstrip())

try:
	ts1Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("[C]: Client socket created")
except:
	print('socket open error: {} \n'.format(err))
	exit()


ts1_addr = socket.gethostbyname(ts1Hostname) 
print("ADDRESS: "+ts1_addr)

ts1_binding = (ts1_addr, int(ts1ListenPort_a))
ts1Sock.connect(ts1_binding)

try:
	ts2Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("[C]: Client socket created")
except:
	print('socket open error: {} \n'.format(err))
	exit()


ts2_addr = socket.gethostbyname(ts2Hostname) 
print("ADDRESS: "+ts1_addr)

ts2_binding = (ts2_addr, int(ts2ListenPort_a))
ts2Sock.connect(ts2_binding)


for cd in cdPairs:
	challenge = cd.split('-')[0]
	clientDigest = cd.split('-')[1]
	print("sending to TS servers: "+challenge)

	ts1Sock.sendall("challenge "+challenge+',')
	ts2Sock.sendall("challenge "+challenge+',')

	ts1Response = ts1Sock.recv(1024)
	ts2Response = ts2Sock.recv(1024)

	print("RECVD FROM TS1: "+ ts1Response)
	print("RECVD FROM TS2: "+ ts2Response)

	if ts1Response == clientDigest:
		sendBack.append("ts1 "+ts1Hostname)
	elif ts2Response == clientDigest:
		sendBack.append("ts2 "+ts2Hostname)

ts1Sock.sendall("finish")
ts2Sock.sendall("finish")

print("SENDING BACK TO CLIENT: "+ str(sendBack))

finalSendBack = ",".join(sendBack)

clientConn.sendall(finalSendBack)
















