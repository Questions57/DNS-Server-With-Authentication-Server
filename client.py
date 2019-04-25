import socket
import sys
import hmac



def sendQuery(serverName, tsHostname, ts1ListenPort_c, ts2ListenPort_c, query):
	print("sending "+query+" to "+serverName)
	try:
		cs2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("[C]: Client socket created")
	except:
		print('socket open error: {} \n'.format(err))
		exit()

	port = 0
	if serverName == "ts1":
		port = int(ts1ListenPort_c)
	else:
		port = int(ts2ListenPort_c)

	tsHostAddress = socket.gethostbyname(tsHostname)
	tsBinding = (tsHostAddress, port)

	cs2.connect(tsBinding)
	print("Connected to "+serverName)

	cs2.sendall(query)
	data = cs2.recv(1024)
	print("DATA RECEIVED FROM "+serverName+": "+data)

	cs2.close()
	return data



inputLines = []
file = open("PROJ3-HNS.txt", "r")

#looping through each line to fill table info
for line in file: 
	inputLines.append(line)

file.close() 
print(inputLines)

try:
	cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("[C]: Client socket created")
except:
	print('socket open error: {} \n'.format(err))
	exit()

asHostname = sys.argv[1]
asListenPort = sys.argv[2]
ts1ListenPort_c = sys.argv[3]
ts2ListenPort_c = sys.argv[4]


as_host_addr = socket.gethostbyname(asHostname) #address of RS host
print("ADDRESS: "+as_host_addr)

as_binding = (as_host_addr, int(asListenPort))
cs.connect(as_binding)

queries = []

for line in inputLines:
	key = line.split(' ')[0]
	challenge = line.split(' ')[1]
	query = line.split(' ')[2].lower()
	queries.append(query)

	createDigest = hmac.new(key.encode("utf-8"), challenge.encode("utf-8"))
	digest = createDigest.hexdigest()

	cs.sendall(challenge+'-'+digest+",")

cs.sendall("finish")

print("finished sending")

data = cs.recv(1024)
print("DATA: "+data)
tldData = data.split(',')

results = [] 

ts1Hostname = ""
ts2Hostname = ""

for line in tldData:
	serverName = line.split(' ')[0]
	tsHostname = line.split(' ')[1]

	if serverName == 'ts1':
		ts1Hostname = tsHostname
	else:
		ts2Hostname = tsHostname

cs_ts1 = None
if ts1Hostname != "":
	try:
		cs_ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("[C]: Client socket created")
	except:
		print('socket open error: {} \n'.format(err))
		exit()


	ts1HostAddress = socket.gethostbyname(ts1Hostname)
	ts1Binding = (ts1HostAddress, int(ts1ListenPort_c))

	cs_ts1.connect(ts1Binding)
	print("Connected to TS1")

cs_ts2 = None
if ts2Hostname != "":
	try:
		cs_ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("[C]: Client socket created")
	except:
		print('socket open error: {} \n'.format(err))
		exit()


	ts2HostAddress = socket.gethostbyname(ts2Hostname)
	ts2Binding = (ts2HostAddress, int(ts2ListenPort_c))

	cs_ts2.connect(ts2Binding)
	print("Connected to TS2")

count = 0
for line in tldData:
	print("TLD data line: "+line)
	serverName = line.split(' ')[0]
	tsHostname = line.split(' ')[1]
	query = queries[count].rstrip()

	print("query to send: "+query)
	
	if serverName == "ts1":
		print("sending "+query+" to TS1")
		cs_ts1.sendall(query)
		ts1Response = cs_ts1.recv(1024)
		results.append(ts1Response)

	if serverName == "ts2":
		print("sending "+query+" to TS2")
		cs_ts2.sendall(query)
		ts2Response = cs_ts2.recv(1024)
		results.append(ts2Response)


	count += 1

if ts1Hostname != "":
	print("sending FINISH to ts1")
	cs_ts1.sendall("finish")

if ts2Hostname != "":
	print("sending FINISH to ts2")
	cs_ts2.sendall("finish")

print("RESULTS: "+str(results))


outputFile = open("RESOLVED.txt", "w")


for line in results:
	outputFile.write(line+"\n")

outputFile.close()








