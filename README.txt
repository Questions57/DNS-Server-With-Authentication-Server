Adarsh Patel  aap237
Shiv Rattan   ssr108


1.) For the challenge response query, we took a simple approach in the authentication server and just iterating through both ts1 and ts2 and responding to the challenges that are given to them. A recursive query puts burden of the name resolution on the called server. In our program, the socket is created in the client and then connected through the open port with the root server. After binding, listening, and accepting are all over, the root server checks its own table to see if there is a match with the hostnames. If it was a match, it outputs the string as is. If not, the client goes to either TS_edu or TS_com to look for the queried hostname. 


2.) There doesn't seem to be any gaping holes with our code. In our testing, the code seems to work perfectly fine and smoothly from the instructions provided. 

3.) A major component on creating any project is communication, and since both of us are college students, it was hard to make our schedules align and get the program done as quickly as possible. 

A problem that we ran in to when designing this code was how to deal with was how to deal with the challenge response part of the authentication server and seending multiple messages. When we wanted to send an entire list of information to one of the servers through the socket, the connection would close after one message being sent in a loop. We ended up figuring out how to send multiple messages and this issue was resolved.

But apart from that, another problem that we faced when creating the algorithm for the code was understanding how we were going to store and traverse through the different challenge-responses, host names, domain names, and DNS records.

4.) This project gave insight on how a lightweight version of DNS would work if it were recursive and had basic cryptographic functions. It was really interesting to see how some of the most integral parts of modern day Internet are so simple in their foundation, but made more complex through possible edge-cases (i.e. security, data corruption, reliable transfers, etc).


